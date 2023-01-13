#!/usr/bin/env groovy

// library identifier: 'jenkins-shared-library@main', retriever: modernSCM (
//     [$class: 'GitSCMSource',
//       remote: 'https://gitlab.com/saymolet/jenkins-shared-library.git',
//       credentialsId: 'gitlab-credentials'
//     ]
// )

pipeline {
    agent none

    stages {
        stage("increment_version") {
            agent {
                docker {
                    image 'python:3.10-slim-buster'
                }
            }
            steps {
                script {
                    sh "pip install poetry"
                    // TODO: install poetry
                    sh "poetry version minor"

                    def version = sh "IFS=' ' read -r -a array <<< `poetry version | sed -r 's/\\x1B\\[([0-9]{1,3}(;[0-9]{1,2};?)?)?[mGK]//g'`; echo ${array[1]}"
                    def name = sh "IFS=' ' read -r -a array <<< `poetry version | sed -r 's/\\x1B\\[([0-9]{1,3}(;[0-9]{1,2};?)?)?[mGK]//g'`; echo ${array[0]}"
                    env.IMAGE_NAME = "$name-$version-$BUILD_NUMBER"
                    sh "echo $IMAGE_NAME"
                }
            }
        }

        stage ("Check version")
            steps {
                script {
                sh 'cat pyproject.toml'
                }
            }

//         stage("build and push docker image") {
//             steps {
//                 script {
//                     buildImage "saymolet/my-repo:$IMAGE_NAME"
//                     // credentials id from Jenkins
//                     dockerLogin "dockerhub-credentials"
//                     dockerPush "saymolet/my-repo:$IMAGE_NAME"
//                 }
//             }
//         }
//
//         stage ("deploy to ec2") {
//             steps {
//                 script {
//                     echo "Deploying to EC2 instance"
//                     // direct docker command
// //                     def dockerCmd = "docker run -d -p 3000:3000 saymolet/my-repo:$IMAGE_NAME"
//
//                     // ssh agent plugin in Jenkins
//                     // ec2-server-key - credential in Jenkins
// //                     def dockerComposeCmd = "docker-compose -f docker-compose.yaml up --detach"
//
//                     // shell commands
//                     // passing newest image name to shell script
//                     def shellCmd = "bash ./server-commands.sh saymolet/my-repo:${IMAGE_NAME}"
//
//                     def ec2_instance = "ec2-user@35.158.120.145"
//
//                     sshagent(['ec2-server-key']) {
//                         // Run docker commands directly on ec2 server
// //                         sh "ssh -o StrictHostKeyChecking=no ${ec2_instance} ${dockerCmd}"
//
//                         // copy docker compose file with secure copy to ec2 server
// //                         sh "scp docker-compose.yaml ${ec2_instance}:/home/ec2-user"
// //                         sh "ssh -o StrictHostKeyChecking=no ${ec2_instance} ${dockerComposeCmd}"
//
//                         // shell script
//                         sh "scp docker-compose.yaml ${ec2_instance}:/home/ec2-user"
//                         sh "scp server-commands.sh ${ec2_instance}:/home/ec2-user"
//                         sh "ssh -o StrictHostKeyChecking=no ${ec2_instance} ${shellCmd}"
//
//                     }
//                 }
//             }
//         }
//
//         stage("commit version update") {
//             steps {
//                 script {
//                     // first - credentials id in Jenkins, second - where to push. Repo url, omitting the https protocol
//                     gitLoginRemote "gitlab-credentials", "gitlab.com/saymolet/node-project.git"
//                     // email and username for jenkins. Displayed with commit
//                     gitConfig "jenkins@example.com", "jenkins"
//                     // branch where to push and message with commit
//                     gitAddCommitPush "master", "ci: version bump"
//                 }
//             }
//         }
//     }
// }