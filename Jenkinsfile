pipeline {

    agent any

    stages {

        stage('Build Docker Containers') {

            steps {

                sh 'docker compose up --build -d'
            }
        }

        stage('Check Running Containers') {

            steps {

                sh 'docker ps'
            }
        }
    }

    post {

        success {

            echo 'Pipeline executed successfully!'
        }

        failure {

            echo 'Pipeline failed!'
        }
    }
}