pipeline {
    agent any
    environment {
        ENV_FILE = credentials('mysql-env')
    }
    
    parameters {
        file(name: 'INIT_DB_SQL', description: 'Upload the SQL file for database initialization')
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

        stage('create-env-file') {
            steps {
                sh 'cp $ENV_FILE .env'
            }
        }

        stage('copy-init-db-sql') {
            steps {
                // Copy INIT_DB_SQL parameter to the workspace as init_db.sql
                sh "cp '${params.INIT_DB_SQL}' ./init_db.sql"
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

        stage('Prepare Deployment') {
            steps {
                sh 'ls -l ./init_db.sql'
            }
        }

        stage('build-production-image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    sh 'docker build -f app/Dockerfile -t ngsharna/flask-app:latest app'
                    sh 'docker push ngsharna/flask-app:latest'
                }
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
        always {
            sh 'docker rm -f test_container'
            junit '**/report.xml'
        }
        failure {
            echo 'The build has failed!'
        }
        success {
            echo 'The build has succeeded!'
        }
    }
}
