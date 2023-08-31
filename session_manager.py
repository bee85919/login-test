from datetime import datetime, timedelta

class SessionManager:
    def __init__(self, db):
        # Database 객체를 받아서 초기화
        self.db = db

    def create_session(self, email, session):
        # 랜덤 토큰 생성
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        # 데이터베이스에 세션 정보 저장
        self.db.create_session(email, token)
        # 세션 변수 설정
        session['email'] = email
        session['token'] = token
        session['created_time'] = datetime.now()

    def is_logged_in(self, session):
        # 로그인 상태 확인
        if 'token' in session:
            session_data = self.db.get_session(session['token'])
            if session_data:
                # 토큰 유효 시간 확인 (15분)
                if datetime.now() - session_data['created_time'] < timedelta(minutes=15):
                    return True
        return False

    def verify_token(self, token, session):
        # 토큰 검증
        session_data = self.db.get_session(token)
        if session_data:
            # 세션 정보와 전달된 토큰 비교
            if session_data['token'] == session['token']:
                return True
        return False
