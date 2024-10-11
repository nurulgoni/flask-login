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

        stage('Prepare Deployment') {
            steps {
                sh 'ls -l ./init_db.sql'
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
