pipeline {
    agent any
    environment {
        ENV_FILE = credentials('mysql-env')  // Reference the secret file by its ID
    }
    
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
                  . $ENV_FILE && docker run \
                  -e MYSQL_HOST=$MYSQL_HOST \
                  -e MYSQL_USER=$MYSQL_USER \
                  -e MYSQL_PASSWORD=$MYSQL_PASSWORD \
                  -e MYSQL_DATABASE=$MYSQL_DATABASE \
                  -e MYSQL_PORT=$MYSQL_PORT \
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

        stage('build-production-image') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    sh 'docker build -f app/Dockerfile -t ngsharna/flask-app:latest app'
                    sh 'docker push ngsharna/flask-app:latest'
                }
            }
        }

        stage('create-env-file') {
            steps {
                script {
                    def envContent = """
                    MYSQL_USER=${env.MYSQL_USER}
                    MYSQL_PASSWORD=${env.MYSQL_PASSWORD}
                    MYSQL_DATABASE=${env.MYSQL_DATABASE}
                    MYSQL_HOST=${env.MYSQL_HOST}
                    MYSQL_PORT=${env.MYSQL_PORT}
                    MYSQL_ROOT_PASSWORD=${env.MYSQL_ROOT_PASSWORD}
                    """.trim() // Remove any surrounding whitespace, newlines

                    writeFile file: '.env', text: envContent
                }
            }
        }

        stage('deploy') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                sh '''
                docker-compose down   
                docker-compose up -d  
                '''
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
