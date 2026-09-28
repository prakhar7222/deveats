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
                sh 'docker compose up -d'
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
