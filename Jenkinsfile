#!/usr/bin/env groovy

library identifier: 'jenkins-shared-library@main', retriever: modernSCM (
    [$class: 'GitSCMSource',
      remote: 'https://gitlab.com/saymolet/jenkins-shared-library.git',
      credentialsId: 'gitlab-credentials'
    ]
)

pipeline {
    agent any

    stages {
        stage("increment_version") {
            steps {
                script {
                    // install python3 and poetry separately on jenkins
                    // docker exec -it -u 0 {jenkins_container_id} bash
                    // apt install python3
                    // apt install python3-pip
                    // pip install poetry

                    sh "poetry version minor"
                    sh "chmod u+x ./scripts/find_name_version.sh"
                    def name = sh(script: "./scripts/find_name_version.sh 0", returnStdout: true).trim()
                    def version = sh(script: "./scripts/find_name_version.sh 1", returnStdout: true).trim()

                    env.IMAGE_NAME = "$name-$version-$BUILD_NUMBER"
                    sh "echo $IMAGE_NAME"
                }
            }
        }

        stage("build and push docker image") {
            steps {
                script {
                    buildImage "saymolet/my-repo:$IMAGE_NAME"
                    // credentials id from Jenkins
                    dockerLogin "dockerhub-credentials"
                    dockerPush "saymolet/my-repo:$IMAGE_NAME"
                }
            }
        }

        stage ("deploy to ec2") {
            steps {
                script {
                    echo "Deploying to EC2 instance"
                    // install docker, docker-compose and do docker login beforehand on EC2
                    // passing newest image name to shell script
                    def shellCmd = "bash ./ec2_deploy.sh saymolet/my-repo:${IMAGE_NAME}"
                    // ec2 IP will change from instance to instance
                    def ec2_instance = "ec2-user@3.71.91.7"

                    // do first login manually to avoid any failed authentications
                    // ssh agent plugin in Jenkins
                    sshagent(['ec2-server-key']) {
                        // copy compose and script
                        sh "scp docker-compose.yaml ${ec2_instance}:/home/ec2-user"
                        sh "scp ./scripts/ec2_deploy.sh ${ec2_instance}:/home/ec2-user"
                        sh "ssh -o StrictHostKeyChecking=no ${ec2_instance} ${shellCmd}"
                    }
                }
            }
        }

        stage("commit version update") {
            steps {
                script {
                    // first - credentials id in Jenkins, second - where to push. Repo url, omitting the https protocol
                    // use fine-grained token instead of a password to authenticate to github
                    gitLoginRemote "github-fine-token", "github.com/saymolet/ml-flask.git"
                    // email and username for jenkins. Displayed with commit
                    gitConfig "jenkins@example.com", "jenkins"
                    // branch where to push and message with commit
                    gitAddCommitPush "main", "ci: version bump"
                }
            }
        }
    }
}