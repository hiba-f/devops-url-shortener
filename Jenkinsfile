node {

    stage('Clone') {
        echo 'Repository cloned successfully'
    }

    stage('Build Docker Image') {
        sh 'docker build -t url-shortener .'
    }

    stage('Check Docker') {
        sh 'docker images'
    }

    stage('Success') {
        echo 'Pipeline executed successfully!'
    }
}