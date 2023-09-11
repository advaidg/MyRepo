pipeline {
    agent any

    environment {
        SONARQUBE_URL = 'http://your-sonarqube-server-url'
        API_TOKEN = 'your-api-token'
        PORTFOLIO_KEY = 'your-portfolio-key'
        QUALITY_GATES = ['A', 'B', 'C']
    }

    stages {
        stage('Fetch Quality Gate Counts') {
            steps {
                script {
                    def projectCountMap = [:]

                    for (qualityGate in QUALITY_GATES) {
                        def apiUrl = "${SONARQUBE_URL}/api/components/search?qualifiers=TRK&gate=${qualityGate}&portfolio=${PORTFOLIO_KEY}"
                        def curlCommand = """curl -s -H 'Authorization: Bearer ${API_TOKEN}' ${apiUrl}"""
                        def response = sh(script: curlCommand, returnStatus: true)

                        if (response == 0) {
                            def responseData = sh(script: curlCommand, returnStdout: true).trim()
                            def projects = responseData.readJSON().components
                            def projectCount = projects.size()
                            projectCountMap[qualityGate] = projectCount
                        } else {
                            error "Failed to fetch data for Quality Gate ${qualityGate} from SonarQube."
                        }
                    }

                    // Print the project counts for each quality gate
                    for (qualityGate in QUALITY_GATES) {
                        echo "Quality Gate ${qualityGate}: ${projectCountMap[qualityGate]} projects"
                    }
                }
            }
        }
    }
}
