@Library('jenkins-pipeline-scripts') _
pipeline {
    agent none
    options {
        // Keep the 50 most recent builds
        buildDiscarder(logRotator(numToKeepStr:'50'))
    }
    stages {
        stage('Build') {
            agent any
            steps {
                sh 'make docker-image'
            }
        }
        stage('Push image to registry') {
            agent any
            steps {
                pushImageToRegistry (
                    env.BUILD_ID,
                    "iadelib/citizenportal"
                )
            }
        }
        stage('Deploy to staging') {
            agent any
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                sh "mco shell run 'docker pull docker-staging.imio.be/iadelib/citizenportal:$BUILD_ID' -I /^pm-staging.imio.be/"
                sh "mco shell run 'systemctl restart website-conseil.service' -t 1200 --tail -I /^pm-staging.imio.be/"
            }
        }
        stage('Deploy to prod ?') {
            agent none
            steps {
                timeout(time: 24, unit: 'HOURS') {
                    input (
                        message: 'Should we deploy to prod ?'
                    )
                }
            }
            post {
                aborted {
                    echo 'In post aborted'
                }
                success {
                    echo 'In post success'
                }
            }
        }
        stage('Deploying to prod') {
            agent any
            steps {
                sh "docker pull docker-staging.imio.be/iadelib/citizenportal:latest-$BUILD_ID"
                sh "docker tag docker-staging.imio.be/iadelib/citizenportal:latest-$BUILD_ID docker-prod.imio.be/iadelib/citizenportal:latest"
                sh "docker push docker-prod.imio.be/iadelib/citizenportal:latest"
                sh "mco shell run 'docker pull docker-prod.imio.be/iadelib/citizenportal:latest' -I /^pm-prod19.imio.be/"
                sh "mco shell run 'systemctl restart website-conseil.service' -t 1200 --tail -I /^pm-prod19.imio.be/"
            }
        }
    }
}
