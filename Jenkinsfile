pipeline {
    agent any

    parameters {
        file(name: 'INIT_DB_SQL', description: 'Upload the SQL file for database initialization')
    }

    stages {
        stage('checkout') {
            steps {
                git branch: 'test', url: 'https://github.com/nurulgoni/flask-login.git'
            }
        }

        stage('copy-init-db-sql') {
            steps {
                script {
                    echo "INIT_DB_SQL parameter: ${params.INIT_DB_SQL}"

                    // Check if the INIT_DB_SQL parameter is set
                    if (params.INIT_DB_SQL != null) {
                        sh "cp '${params.INIT_DB_SQL}' ./init_db.sql"
                        echo "SQL file copied as init_db.sql"
                    } else {
                        error "INIT_DB_SQL parameter is not set or is empty."
                    }
                }
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
