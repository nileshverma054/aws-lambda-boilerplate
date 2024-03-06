def (awsRoleAccount, awsRole, releaseEnv) = getEnvDetails();
echo "Build Environment: ${releaseEnv}"

pipeline {
    agent {
        docker {
                image 'public.ecr.aws/sam/build-python3.9:1.105.0-20231212200228'
                args '-e HOME=/var/tmp'
            }
    }
    environment {
        SAM_CLI_TELEMETRY = 0
    }
     stages {
        stage('Tests') {
            steps { 
                echo 'Test - To be implemented' 
            }
        }
        stage('integration'){
            when { 
                expression { releaseEnv == 'integration' } 
                }
            steps { 
                echo 'Running integration build' 
            }
        }
        stage('qa'){
            when { 
                expression { releaseEnv == 'qa' } 
                }
            steps { 
                echo 'Running qa build' 
            }
        }
        stage('staging'){
            when { 
                expression { releaseEnv == 'staging' } 
                }
            steps { 
                echo 'Running staging build' 
            }
        }
        stage('production'){
            when { 
                expression { releaseEnv == 'production' } 
                }
            steps { 
                echo 'Running production build' 
            }
        }

        stage('Build'){
            steps {
                echo "Creating SAM Build"
                sh """
                sam --version
                sam build -t sam/template.yaml
                """
            }
        }
        stage("Deploy") {
            steps {           
                echo "Deploying SAM Build"
                withAWS(roleAccount: awsRoleAccount, role: awsRole) {
                    sh """
                    sam deploy --config-file ${WORKSPACE}/sam/samconfig.toml --config-env ${releaseEnv}
                    """
                }
            }
        }
    }
    post {
            always {
                notifyBuild(currentBuild.currentResult, releaseEnv)
                cleanWs()
            }
        }
}

def notifyBuild(String buildStatus, String releaseEnv) {
    emailext (
        mimeType: "text/html",
        subject: "Lambda Function Deployment | ${releaseEnv} Env: ${buildStatus}",
        body: "Job ${env.JOB_NAME} build #${env.BUILD_NUMBER} Build status: ${buildStatus}\n More info at: ${env.BUILD_URL}",
        to: "user1@example.com,user2@example.com"
    )
}

def getEnvDetails() {
    def roleAccount, role, releaseEnv;
    echo "build branch: ${env.BRANCH_NAME}"
    switch(env.BRANCH_NAME) {
        case "lambda-integration":
            roleAccount = "123456789"
            role = "arn:aws:iam::123456789:role/jenkins-cloudformation-update"
            releaseEnv = "integration"
            break
        case "lambda-qa":
            roleAccount = "123456789"
            role = "arn:aws:iam::123456789:role/qa-jenkins-cloudformation-update"
            releaseEnv = "qa"
            break
        case ~/(^rc.+)/:
            roleAccount = "123456789"
            role = "arn:aws:iam::123456789:role/stg-jenkins-cloudformation-update"
            releaseEnv = "staging"
            break
        case ~/(^v.+)/:
            roleAccount = "123456789"
            role = "arn:aws:iam::123456789:role/us-jenkins-cloudformation-update"
            releaseEnv = "production"
            break
        case ~/^dev-.+/:
            roleAccount = "123456789"
            role = "arn:aws:iam::123456789:role/jenkins-cloudformation-update"
            releaseEnv = "integration"
            break
        default:
            echo "[${env.BRANCH_NAME}] is not a valid branch for build, Aborting!"
            exit 1
    }
    return [roleAccount, role, releaseEnv]
}
