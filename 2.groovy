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

                    try {
                        // Execute a shell command using curl
                        def portfolioResponse = sh(
                            script: """
                                curl -s -k -H "Authorization: Bearer \${SONARQUBE_TOKEN}" \\
                                "${SONARQUBE_URL}/api/projects/index?portfolio=${portfolioName}"
                            """,
                            returnStatus: true,
                            returnStdout: true
                        )

                        if (portfolioResponse == 0) {
                            def portfolioProjects = sh(
                                script: """
                                    curl -s -k -H "Authorization: Bearer \${SONARQUBE_TOKEN}" \\
                                    "${SONARQUBE_URL}/api/projects/index?portfolio=${portfolioName}" | jq -r '.projects[] | .analysisId'
                                """,
                                returnStdout: true
                            ).trim().split('\n')

                            portfolioProjects.each { analysisId ->
                                def qualityGateStatus = sh(
                                    script: """
                                        curl -s -k -H "Authorization: Bearer \${SONARQUBE_TOKEN}" \\
                                        "${SONARQUBE_URL}/api/qualitygates/project_status?analysisId=${analysisId}" |
                                        jq -r '.projectStatus.status'
                                    """,
                                    returnStdout: true
                                ).trim()

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
                        } else {
                            error("Error: Failed to fetch portfolio data.")
                        }
                    } catch (Exception e) {
                        error("Error: ${e.message}")
                    }
                }
            }
        }
    }
}
