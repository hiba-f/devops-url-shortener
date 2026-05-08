node {

    stage('Build Docker Containers') {

        sh 'docker-compose up --build -d'
    }

    stage('Check Running Containers') {

        sh 'docker ps'
    }
}