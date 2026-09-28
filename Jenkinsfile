pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Start Services') {
            steps {
                sh '''
                    docker ps -q --filter "publish=5000" | xargs -r docker rm -f
                    docker ps -q --filter "publish=8081" | xargs -r docker rm -f
                    docker compose up -d --wait
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker compose exec -T backend pytest -v'
            }
        }
    }

    post {
        always {
            sh 'docker compose ps || true'
            sh 'docker compose down -v || true'
        }

        success {
            echo 'DevEats CI pipeline completed successfully!'
        }

        failure {
            echo 'DevEats pipeline failed!'
        }
    }
}
