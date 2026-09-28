pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Tests') {
            steps {
                dir('backend') {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        pytest -v
                    '''
                }
            }
        }

    }

    post {
        success {
            echo 'DevEats CI pipeline completed successfully!'
        }

        failure {
            echo 'DevEats CI pipeline failed!'
        }
    }
}
