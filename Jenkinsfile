pipeline {
    agent any
    
    stages {
        stage('checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/nurulgoni/flask-login.git'
            }
        }

        stage('build') {
            steps {
                sh 'docker build -f Dockerfile.test -t flask-test:latest .'
            }
        }

        stage('test') {
            steps {
                sh '''
                docker run \
                  -e MYSQL_HOST=localhost \
                  -e MYSQL_USER=flask \
                  -e MYSQL_PASSWORD=password \
                  -e MYSQL_DATABASE=geeklogin \
                  -e MYSQL_PORT=3306 \
                  -e REPORT_TYPE=junit \
                  -v "$(pwd)":/output \
                  --name test_container flask-test:latest
                '''
            }
        }

        stage('report-generate') {
            steps {
                sh 'docker cp test_container:/mysql_login/report.xml ./report.xml'
            }
        }
    }
    post {
    always {
        sh 'docker rm -f test_container'   // Fail if container removal fails
        junit '**/report.xml'              // Archive test reports
    }
    failure {
        echo 'The build has failed!'
    }
    success {
        echo 'The build has succeeded!'
    }
}

}
