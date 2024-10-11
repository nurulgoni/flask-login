pipeline {
    agent any
    environment {
        ENV_FILE = credentials('mysql-env')
    }
    

    parameters {
        base64File description: 'Upload the database file', name: 'INIT_DB_SQL'
    }

    stages {
        stage('checkout') {
            steps {
                git branch: 'test', url: 'https://github.com/nurulgoni/flask-login.git'
            }
        }

        stage('copy-init-db-sql') {
            steps {
                withFileParameter('INIT_DB_SQL') {
                    sh 'cat $INIT_DB_SQL > init_db.sql'
                }
            }
        }

        stage('create-env-file') {
            steps {
                sh 'cp $ENV_FILE .env'
            }
        }
        stage('build-test') {
            steps {
                sh 'docker build -f Dockerfile.test -t flask-test:latest .'
            }
        }

        stage('testing') {
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

        stage('Prepare Deployment') {
            steps {
                sh 'ls -l ./init_db.sql'
            }
        }

        stage('deploy') {
            steps {
                sh '''
                docker-compose down   
                docker-compose up -d  
                '''
            }
        }
    }

    post {
        failure {
            echo 'The build has failed!'
        }
        success {
            echo 'The build has succeeded!'
        }
    }
}
