pipeline {
  agent any

  // 매일 15:40 (Asia/Seoul) 실행
  triggers {
    cron('''TZ=Asia/Seoul
40 15 * * *''')
  }

  options {
    // 로그 너무 길어지는 것 방지(선택)
    buildDiscarder(logRotator(numToKeepStr: '20'))
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup venv & deps (Windows)') {
      when { expression { !isUnix() } } // 윈도우에서만 실행
      steps {
        bat '''
        if not exist .venv (
          "C:\\Python\\Python312\\python.exe" -m venv .venv
        )
        .venv\\Scripts\\python -m pip install --upgrade pip
        if exist requirements.txt (
          .venv\\Scripts\\pip install -r requirements.txt
        )
        '''
      }
    }

    stage('Run script (Windows)') {
      when { expression { !isUnix() } }
      steps {
        // 스크립트 이름/경로를 네가 쓰는 것으로 바꿔!
        bat '''
        .venv\\Scripts\\python main.py
        '''
      }
    }

    // 리눅스/맥 에이전트에서도 돌릴 수 있게 병행 제공 (선택)
    stage('Setup venv & deps (Linux/Mac)') {
      when { expression { isUnix() } }
      steps {
        sh '''
        python3 -m venv .venv || true
        . .venv/bin/activate
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        '''
      }
    }

    stage('Run script (Linux/Mac)') {
      when { expression { isUnix() } }
      steps {
        sh '''
        . .venv/bin/activate
        python main.py
        '''
      }
    }
  }

  post {
    always {
      // (선택) 로그/결과물 보관 예시
      archiveArtifacts artifacts: 'logs/**/*.log', allowEmptyArchive: true
    }
    failure {
      // (선택) 실패 시 배지/노티 연동 가능(이메일/슬랙 등)
      echo 'Job failed.'
    }
  }
}
