node {

    stage('Build Flask Image') {

        sh 'docker build -t url-shortener ./app'
    }

    stage('Run Redis Container') {

        sh 'docker run -d --name redis -p 6379:6379 redis || true'
    }

    stage('Run Flask Container') {

        sh """
        docker run -d \
        --name flask-app \
        -p 5000:5000 \
        --link redis \
        url-shortener || true
        """
    }

    stage('Check Running Containers') {

        sh 'docker ps'
    }
}