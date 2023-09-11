pipeline {
    agent any
 
    parameters {
        string(name: 'PORTFOLIO_NAME', description: 'Enter the portfolio name:')
    }
 
    stages {
        stage('Count Quality Gates') {
            steps {
                script {
                    def portfolioName = params.PORTFOLIO_NAME
                    def qualityGateCounts = [:]
                    
                    // Disable SSL certificate verification
                    def httpClient = new groovyx.net.http.RESTClient('https://your-sonarqube-url.com')
                    httpClient.client.skipSSLIssues()
                    
                    try {
                        // Fetch projects within the portfolio
                        def portfolioResponse = httpClient.get(
                            path: "/api/projects/index?portfolio=${portfolioName}",
                            headers: ['Authorization': "Bearer ${env.SONARQUBE_TOKEN}"]
                        )
                        def portfolioProjects = portfolioResponse.data.projects
                        
                        // Loop through projects and count quality gates
                        portfolioProjects.each { project ->
                            def qualityGateResponse = httpClient.get(
                                path: "/api/qualitygates/project_status?analysisId=${project.analysisId}",
                                headers: ['Authorization': "Bearer ${env.SONARQUBE_TOKEN}"]
                            )
                            def qualityGateStatus = qualityGateResponse.data.projectStatus.status
                            
                            if (qualityGateStatus in ['A', 'B', 'C', 'D', 'E', 'F']) {
                                qualityGateCounts[qualityGateStatus] = (qualityGateCounts[qualityGateStatus] ?: 0) + 1
                            }
                        }
                        
                        // Print the quality gate counts
                        echo "Quality Gate Counts for Portfolio '${portfolioName}':"
                        echo "A: ${qualityGateCounts.A ?: 0}"
                        echo "B: ${qualityGateCounts.B ?: 0}"
                        echo "C: ${qualityGateCounts.C ?: 0}"
                        echo "D: ${qualityGateCounts.D ?: 0}"
                        echo "E: ${qualityGateCounts.E ?: 0}"
                        echo "F: ${qualityGateCounts.F ?: 0}"
                    } catch (Exception e) {
                        error("Error: ${e.message}")
                    }
                }
            }
        }
    }
}
