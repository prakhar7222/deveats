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

        stage('Wait for Database') {
            steps {
                sh '''
                    echo "Waiting for PostgreSQL..."

                    for i in $(seq 1 30); do
                        if docker compose exec -T database pg_isready -U deveats -d deveats; then
                            echo "PostgreSQL is ready!"
                            break
                        fi

                        echo "PostgreSQL not ready yet... attempt $i/30"
                        sleep 2

                        if [ "$i" -eq 30 ]; then
                            echo "PostgreSQL failed to become ready"
                            docker compose logs database
                            exit 1
                        fi
                    done
                '''
            }
        }

        stage('Wait for Backend') {
            steps {
                sh '''
                    echo "Waiting for Backend..."

                    for i in $(seq 1 30); do
                        if docker compose exec -T backend python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health', timeout=2)" >/dev/null 2>&1; then
                            echo "Backend is ready!"
                            break
                        fi

                        echo "Backend not ready yet... attempt $i/30"
                        sleep 2

                        if [ "$i" -eq 30 ]; then
                            echo "Backend failed to become ready"
                            docker compose logs backend
                            exit 1
                        fi
                    done
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker compose exec -T backend pytest -v'
            }
        }

        stage('Health Check') {
            steps {
                sh 'docker compose exec -T backend python -c "import urllib.request; print(urllib.request.urlopen(\"http://localhost:5000/api/health\").read().decode())"'
            }
        }
    }

    post {
        always {
            sh 'docker compose ps || true'
            sh 'docker compose logs --tail=50 || true'
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
