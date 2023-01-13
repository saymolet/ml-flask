#!/usr/bin/env groovy

// library identifier: 'jenkins-shared-library@main', retriever: modernSCM (
//     [$class: 'GitSCMSource',
//       remote: 'https://gitlab.com/saymolet/jenkins-shared-library.git',
//       credentialsId: 'gitlab-credentials'
//     ]
// )

pipeline {
    agent any

    stages {
        stage("increment_version") {
            steps {
                script {
                    // install python3 and poetry separately on jenkins
                    sh "poetry version minor"
                    sh "chmod a+x script.sh"
                    def name = sh "./script.sh 0"
                    def version = sh "./script.sh 1"

                    env.IMAGE_NAME = "$name-$version-$BUILD_NUMBER"
                    sh "echo $IMAGE_NAME"
                }
            }
        }

        stage ("Check version") {
            steps {
                script {
                sh 'cat pyproject.toml'
                sh "echo $IMAGE_NAME"
                }
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
    }
}