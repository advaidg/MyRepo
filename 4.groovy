// Define SonarQube server and API token
def SONARQUBE_SERVER = 'http://your-sonarqube-server'
def SONARQUBE_API_TOKEN = 'your-sonarqube-api-token'

pipeline {
    agent any

    stages {
        stage('Input Portfolio Name') {
            steps {
                script {
                    def portfolioName = input(
                        id: 'portfolioName',
                        message: 'Enter the name of the portfolio:',
                        parameters: [string(defaultValue: '', description: 'Portfolio Name', name: 'PORTFOLIO_NAME')]
                    )
                    PORTFOLIO_ID = getPortfolioIdByName(portfolioName)
                }
            }
        }

        stage('Get Project Data') {
            steps {
                script {
                    if (!PORTFOLIO_ID) {
                        error("Portfolio ID not found.")
                    }

                    def qualityGateLabels = ['A', 'B', 'C', 'D', 'E', 'F']

                    for (String qualityGate : qualityGateLabels) {
                        def projectCount = getProjectCountInQualityGate(qualityGate)
                        echo "Quality Gate $qualityGate: $projectCount projects"
                    }
                }
            }
        }
    }
}

def getPortfolioIdByName(String portfolioName) {
    def apiUrl = "${SONARQUBE_SERVER}/api/portfolios/search"
    def apiParams = [
        q: portfolioName,
    ]

    def curlCommand = """
        curl -s -X GET "$apiUrl" \\
        -H "Authorization: Bearer $SONARQUBE_API_TOKEN" \\
        -G --data-urlencode "q=${apiParams.q}"
    """

    def response = bat(script: curlCommand, returnStatus: true).trim()

    if (response == '0') {
        def jsonResponse = bat(script: curlCommand, returnStdout: true).trim()
        def portfolios = readJSON text: jsonResponse
        if (portfolios.portfolios.size() > 0) {
            return portfolios.portfolios[0].uuid
        }
    }

    return null
}

def getProjectCountInQualityGate(String qualityGate) {
    def apiUrl = "${SONARQUBE_SERVER}/api/components/search"
    def apiParams = [
        qualifiers: 'TRK',
        portfolio: PORTFOLIO_ID,
        gate: qualityGate,
    ]

    def curlCommand = """
        curl -s -X GET "$apiUrl" \\
        -H "Authorization: Bearer $SONARQUBE_API_TOKEN" \\
        -G --data-urlencode "qualifiers=${apiParams.qualifiers}" \\
        --data-urlencode "portfolio=${apiParams.portfolio}" \\
        --data-urlencode "gate=${apiParams.gate}"
    """

    def response = bat(script: curlCommand, returnStatus: true).trim()

    if (response == '0') {
        def jsonResponse = bat(script: curlCommand, returnStdout: true).trim()
        def projectCount = readJSON text: jsonResponse
        return projectCount.components.size()
    } else {
        error "Failed to retrieve project data for Quality Gate ${qualityGate}."
    }
}
