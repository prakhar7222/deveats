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

        stage('Health Check') {
            steps {
                sh 'curl -f http://localhost:8081/api/health'
            }
        }
    }

    post {
        always {
            sh 'docker compose ps || true'
        }

        success {
            echo 'DevEats CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'DevEats pipeline failed!'
        }
    }
}
