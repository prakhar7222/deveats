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
                sh '''
                    echo "Waiting for frontend..."

                    for i in 1 2 3 4 5 6 7 8 9 10; do
                        if docker compose exec -T frontend wget -qO- http://localhost/api/health; then
                            echo "Health check passed!"
                            exit 0
                        fi

                        echo "Attempt $i failed. Waiting 2 seconds..."
                        sleep 2
                    done

                    echo "Health check failed!"
                    exit 1
                '''
            }
        }
    }

    post {
        always {
            sh 'docker compose ps || true'
            sh 'docker compose down -v || true'
        }

        success {
            echo 'DevEats CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'DevEats pipeline failed!'
        }
    }
}
