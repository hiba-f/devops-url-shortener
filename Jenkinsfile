node {

    stage('Build Image') {
        sh 'docker build -t url-shortener .'
    }

    stage('Run Redis') {
        sh 'docker run -d --name redis redis || true'
    }

    stage('Run Flask') {
        sh 'docker run -d -p 5000:5000 --name flask-app --link redis url-shortener || true'
    }

    stage('Check Containers') {
        sh 'docker ps'
    }
}
