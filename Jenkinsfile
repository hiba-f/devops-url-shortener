pipeline {

    agent any

    stages {

        stage('Clone Repository') {

            steps {

                git 'https://github.com/hiba-f/devops-url-shortener.git'
            }
        }

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
}
