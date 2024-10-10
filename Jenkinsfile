pipeline {
    agent any

    parameters {
        base64File description: 'Upload the database file', name: 'init_db'
    }

    stages {
        stage('checkout') {
            steps {
                git branch: 'test', url: 'https://github.com/nurulgoni/flask-login.git'
            }
        }

        stage('copy-init-db-sql') {
            steps {
                withFileParameter('init_db') {
                    sh 'cat $init_db > init_db.sql'
                }
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
