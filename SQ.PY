import requests
import json
import pandas as pd
from collections import defaultdict
from urllib.parse import urlencode

class SonarQubeExtractor:
    def __init__(self, sonar_url, token, project_key):
        self.sonar_url = sonar_url.rstrip('/')
        self.token = token
        self.project_key = project_key
        self.headers = {'Authorization': f'Bearer {token}'}
    
    def get_all_issues(self, page_size=500):
        """Fetch all issues for the project with pagination"""
        all_issues = []
        page = 1
        
        while True:
            params = {
                'componentKeys': self.project_key,
                'ps': page_size,  # page size
                'p': page,        # page number
                'additionalFields': 'comments,users'
            }
            
            url = f"{self.sonar_url}/api/issues/search"
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                break
                
            data = response.json()
            issues = data.get('issues', [])
            
            if not issues:
                break
                
            all_issues.extend(issues)
            print(f"Fetched page {page}: {len(issues)} issues")
            
            # Check if we've got all pages
            if len(issues) < page_size:
                break
                
            page += 1
        
        return all_issues
    
    def categorize_issues(self, issues):
        """Categorize issues by type, severity, and priority"""
        categorized = {
            'security': {'high': [], 'medium': [], 'low': []},
            'bugs': {'critical': [], 'major': [], 'minor': [], 'info': []},
            'code_smells': {'critical': [], 'major': [], 'minor': [], 'info': []},
            'vulnerabilities': {'critical': [], 'major': [], 'minor': [], 'info': []}
        }
        
        severity_mapping = {
            'BLOCKER': 'critical',
            'CRITICAL': 'critical', 
            'MAJOR': 'major',
            'MINOR': 'minor',
            'INFO': 'info'
        }
        
        security_severity_mapping = {
            'BLOCKER': 'high',
            'CRITICAL': 'high',
            'MAJOR': 'medium', 
            'MINOR': 'low',
            'INFO': 'low'
        }
        
        for issue in issues:
            issue_type = issue.get('type', '').lower()
            severity = issue.get('severity', '')
            
            # Create issue summary
            issue_summary = {
                'key': issue.get('key'),
                'rule': issue.get('rule'),
                'message': issue.get('message'),
                'component': issue.get('component', '').split(':')[-1],  # Get filename
                'line': issue.get('line'),
                'severity': severity,
                'status': issue.get('status'),
                'effort': issue.get('effort', ''),
                'creationDate': issue.get('creationDate'),
                'updateDate': issue.get('updateDate')
            }
            
            if issue_type == 'security_hotspot':
                sec_severity = security_severity_mapping.get(severity, 'low')
                categorized['security'][sec_severity].append(issue_summary)
            elif issue_type == 'vulnerability':
                vuln_severity = severity_mapping.get(severity, 'info')
                categorized['vulnerabilities'][vuln_severity].append(issue_summary)
            elif issue_type == 'bug':
                bug_severity = severity_mapping.get(severity, 'info')
                categorized['bugs'][bug_severity].append(issue_summary)
            elif issue_type == 'code_smell':
                smell_severity = severity_mapping.get(severity, 'info')
                categorized['code_smells'][smell_severity].append(issue_summary)
        
        return categorized
    
    def get_unique_issues_summary(self, categorized_issues):
        """Get unique issues count summary - just rule names and counts"""
        summary = {}
        
        for category, severities in categorized_issues.items():
            summary[category] = {}
            for severity, issues in severities.items():
                # Count occurrences of each unique rule
                rule_counts = {}
                for issue in issues:
                    rule = issue['rule']
                    rule_message = issue['message']
                    
                    if rule not in rule_counts:
                        rule_counts[rule] = {
                            'rule_key': rule,
                            'rule_name': self.get_rule_name(rule),
                            'example_message': rule_message,
                            'count': 0
                        }
                    rule_counts[rule]['count'] += 1
                
                # Sort by count (highest first)
                sorted_rules = sorted(rule_counts.values(), key=lambda x: x['count'], reverse=True)
                
                summary[category][severity] = {
                    'total_issues': len(issues),
                    'unique_rule_types': len(rule_counts),
                    'rules': sorted_rules
                }
        
        return summary
    
    def get_rule_name(self, rule_key):
        """Get human-readable rule name from rule key"""
        try:
            url = f"{self.sonar_url}/api/rules/show"
            params = {'key': rule_key}
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('rule', {}).get('name', rule_key)
        except:
            pass
        
        # Fallback to rule key if API call fails
        return rule_key
    
    def export_to_files(self, categorized_issues, summary):
        """Export results focusing on counts only"""
        
        # Create a clean summary CSV with just counts
        summary_rows = []
        for category, severities in summary.items():
            for severity, data in severities.items():
                for rule in data['rules']:
                    summary_rows.append({
                        'Category': category.replace('_', ' ').title(),
                        'Severity': severity.upper(),
                        'Rule Name': rule['rule_name'],
                        'Rule Key': rule['rule_key'],
                        'Count': rule['count'],
                        'Example Message': rule['example_message'][:100] + '...' if len(rule['example_message']) > 100 else rule['example_message']
                    })
        
        # Sort by count descending
        summary_df = pd.DataFrame(summary_rows)
        summary_df = summary_df.sort_values('Count', ascending=False)
        summary_df.to_csv('sonarqube_rule_counts.csv', index=False)
        
        # Export summary to JSON (counts only)
        with open('sonarqube_rule_counts.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Create category totals
        category_totals = []
        for category, severities in summary.items():
            for severity, data in severities.items():
                if data['total_issues'] > 0:
                    category_totals.append({
                        'Category': category.replace('_', ' ').title(),
                        'Severity': severity.upper(),
                        'Total Issues': data['total_issues'],
                        'Unique Rule Types': data['unique_rule_types']
                    })
        
        totals_df = pd.DataFrame(category_totals)
        totals_df.to_csv('sonarqube_category_totals.csv', index=False)
        
        print("Files exported:")
        print("- sonarqube_rule_counts.csv (rules with counts)")
        print("- sonarqube_rule_counts.json (detailed JSON)")
        print("- sonarqube_category_totals.csv (category summaries)")
    
    def print_summary(self, summary):
        """Print a formatted count-based summary"""
        print("\n" + "="*80)
        print("SONARQUBE UNIQUE ISSUES COUNT SUMMARY")
        print("="*80)
        
        for category, severities in summary.items():
            category_name = category.upper().replace('_', ' ')
            print(f"\n📊 {category_name}")
            print("-" * 60)
            
            for severity, data in severities.items():
                if data['total_issues'] > 0:
                    print(f"\n  {severity.upper()} ({data['total_issues']} total issues, {data['unique_rule_types']} unique types)")
                    print("  " + "-" * 50)
                    
                    # Show top 5 most frequent rules
                    top_rules = data['rules'][:5]
                    for rule in top_rules:
                        rule_name = rule['rule_name'][:45] + "..." if len(rule['rule_name']) > 45 else rule['rule_name']
                        print(f"    • {rule_name:50} → {rule['count']:4} times")
                    
                    if len(data['rules']) > 5:
                        print(f"    ... and {len(data['rules']) - 5} more rule types")
    
    def get_quick_counts_only(self):
        """Quick method to get just the counts without detailed analysis"""
        print("Fetching issue counts...")
        
        # Use facets to get quick counts
        params = {
            'componentKeys': self.project_key,
            'facets': 'rules,severities,types',
            'ps': 1  # We only need facet data, not actual issues
        }
        
        url = f"{self.sonar_url}/api/issues/search"
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            facets = data.get('facets', [])
            
            print("\nQUICK COUNTS:")
            print("=" * 40)
            
            for facet in facets:
                print(f"\n{facet['property'].upper()}:")
                for value in facet['values']:
                    print(f"  {value['val']:20} → {value['count']:4} issues")
        
        return response.json() if response.status_code == 200 else None


def main():
    # Configuration
    SONAR_URL = "http://your-sonarqube-server:9000"  # Replace with your SonarQube URL
    TOKEN = "your-sonarqube-token"  # Replace with your token
    PROJECT_KEY = "your-project-key"  # Replace with your project key
    
    # Initialize extractor
    extractor = SonarQubeExtractor(SONAR_URL, TOKEN, PROJECT_KEY)
    
    # Option 1: Quick counts using facets (fastest)
    print("Getting quick counts...")
    quick_data = extractor.get_quick_counts_only()
    
    # Option 2: Detailed analysis with rule names and counts
    print("\n" + "="*60)
    print("DETAILED ANALYSIS")
    print("="*60)
    
    print("Fetching all issues for detailed analysis...")
    issues = extractor.get_all_issues()
    print(f"Total issues fetched: {len(issues)}")
    
    print("\nCategorizing issues...")
    categorized = extractor.categorize_issues(issues)
    
    print("Generating count summary...")
    summary = extractor.get_unique_issues_summary(categorized)
    
    # Print summary to console
    extractor.print_summary(summary)
    
    # Export to files
    print("\nExporting results...")
    extractor.export_to_files(categorized, summary)

if __name__ == "__main__":
    main()
