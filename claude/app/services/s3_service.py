"""
AWS S3 Service (Back1 Day 3)
파일 업로드/다운로드 서비스
"""
import boto3
from botocore.exceptions import ClientError
from typing import Optional, BinaryIO
from datetime import datetime, timedelta
import os
import uuid
from app.core.config import settings


class S3Service:
    """
    AWS S3 파일 관리 서비스

    기능:
    - 파일 업로드
    - 파일 다운로드 URL 생성
    - 파일 삭제
    - Presigned URL 생성
    """

    def __init__(self):
        """Initialize S3 client"""
        self.bucket_name = getattr(settings, 'AWS_S3_BUCKET', 'artnex-mvp-files')
        self.region = getattr(settings, 'AWS_REGION', 'ap-northeast-2')

        # AWS credentials
        aws_access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
        aws_secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)

        if aws_access_key and aws_secret_key:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=self.region
            )
            self.mock_mode = False
        else:
            print("⚠️  AWS credentials not found. Using mock mode.")
            self.s3_client = None
            self.mock_mode = True

    async def upload_file(
        self,
        file_data: bytes,
        file_name: str,
        folder: str = "uploads",
        content_type: Optional[str] = None
    ) -> dict:
        """
        파일을 S3에 업로드합니다

        Args:
            file_data: 파일 바이트 데이터
            file_name: 파일명
            folder: S3 내 폴더 (e.g., "contracts", "reports", "designs")
            content_type: 파일 MIME 타입

        Returns:
            업로드 결과 딕셔너리
        """
        # Mock mode
        if self.mock_mode:
            return self._mock_upload(file_name, folder, len(file_data))

        try:
            # 고유한 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            file_ext = os.path.splitext(file_name)[1]
            s3_key = f"{folder}/{timestamp}_{unique_id}{file_ext}"

            # Content-Type 추론
            if not content_type:
                content_type = self._guess_content_type(file_name)

            # S3 업로드
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_data,
                ContentType=content_type
            )

            # 파일 URL 생성
            file_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"

            return {
                "success": True,
                "file_url": file_url,
                "s3_key": s3_key,
                "file_name": file_name,
                "file_size": len(file_data),
                "folder": folder,
                "uploaded_at": datetime.now().isoformat()
            }

        except ClientError as e:
            print(f"S3 upload error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "파일 업로드 실패"
            }

    def _mock_upload(self, file_name: str, folder: str, file_size: int) -> dict:
        """Mock 파일 업로드 (개발/테스트용)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        file_ext = os.path.splitext(file_name)[1]
        s3_key = f"{folder}/{timestamp}_{unique_id}{file_ext}"

        mock_url = f"https://mock-s3.artnex.com/{s3_key}"

        return {
            "success": True,
            "file_url": mock_url,
            "s3_key": s3_key,
            "file_name": file_name,
            "file_size": file_size,
            "folder": folder,
            "uploaded_at": datetime.now().isoformat(),
            "mock": True,
            "message": "AWS credentials가 없어 Mock 업로드를 사용합니다"
        }

    def generate_presigned_url(
        self,
        s3_key: str,
        expiration: int = 3600
    ) -> Optional[str]:
        """
        Presigned URL 생성 (임시 다운로드 링크)

        Args:
            s3_key: S3 객체 키
            expiration: 만료 시간 (초)

        Returns:
            Presigned URL 또는 None
        """
        if self.mock_mode:
            return f"https://mock-presigned.artnex.com/{s3_key}?expires={expiration}"

        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=expiration
            )
            return url

        except ClientError as e:
            print(f"Presigned URL generation error: {str(e)}")
            return None

    async def delete_file(self, s3_key: str) -> dict:
        """
        S3에서 파일 삭제

        Args:
            s3_key: S3 객체 키

        Returns:
            삭제 결과
        """
        if self.mock_mode:
            return {
                "success": True,
                "s3_key": s3_key,
                "message": "Mock 파일 삭제 완료",
                "mock": True
            }

        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )

            return {
                "success": True,
                "s3_key": s3_key,
                "message": "파일 삭제 완료"
            }

        except ClientError as e:
            print(f"S3 delete error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "파일 삭제 실패"
            }

    def _guess_content_type(self, file_name: str) -> str:
        """
        파일 확장자로부터 Content-Type 추론

        Args:
            file_name: 파일명

        Returns:
            Content-Type
        """
        ext = os.path.splitext(file_name)[1].lower()

        content_types = {
            '.pdf': 'application/pdf',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime',
            '.avi': 'video/x-msvideo',
            '.zip': 'application/zip',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.txt': 'text/plain',
            '.csv': 'text/csv',
            '.json': 'application/json'
        }

        return content_types.get(ext, 'application/octet-stream')

    async def upload_tutorial_video(
        self,
        video_data: bytes,
        video_name: str
    ) -> dict:
        """
        활용 가이드 영상 업로드

        Args:
            video_data: 영상 바이트 데이터
            video_name: 영상 파일명

        Returns:
            업로드 결과
        """
        return await self.upload_file(
            file_data=video_data,
            file_name=video_name,
            folder="tutorials",
            content_type="video/mp4"
        )

    async def upload_contract(
        self,
        contract_data: bytes,
        contract_name: str
    ) -> dict:
        """
        계약서 업로드

        Args:
            contract_data: 계약서 바이트 데이터
            contract_name: 계약서 파일명

        Returns:
            업로드 결과
        """
        return await self.upload_file(
            file_data=contract_data,
            file_name=contract_name,
            folder="contracts",
            content_type="application/pdf"
        )

    async def upload_report(
        self,
        report_data: bytes,
        report_name: str
    ) -> dict:
        """
        리포트 PDF 업로드

        Args:
            report_data: 리포트 바이트 데이터
            report_name: 리포트 파일명

        Returns:
            업로드 결과
        """
        return await self.upload_file(
            file_data=report_data,
            file_name=report_name,
            folder="reports",
            content_type="application/pdf"
        )


# Singleton instance
s3_service = S3Service()
