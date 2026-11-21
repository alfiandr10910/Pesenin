from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.mahasiswa import Mahasiswa
from app.schemas.mahasiswa import CredentialVerifyRequest, MahasiswaCreate, MahasiswaUpdate


class MahasiswaController:
    @staticmethod
    def create(db: Session, payload: MahasiswaCreate) -> Mahasiswa:
        if db.get(Mahasiswa, payload.nim):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="NIM already exists")
        if db.scalar(select(Mahasiswa).where(Mahasiswa.email == payload.email)):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        mahasiswa = Mahasiswa(
            nim=payload.nim,
            nama_depan=payload.nama_depan,
            nama_belakang=payload.nama_belakang,
            email=payload.email,
            password=hash_password(payload.password),
        )
        db.add(mahasiswa)
        db.commit()
        db.refresh(mahasiswa)
        return mahasiswa

    @staticmethod
    def get_by_nim(db: Session, nim: str) -> Mahasiswa:
        mahasiswa = db.get(Mahasiswa, nim)
        if not mahasiswa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mahasiswa not found")
        return mahasiswa

    @staticmethod
    def list(db: Session) -> list[Mahasiswa]:
        return list(db.scalars(select(Mahasiswa)).all())

    @staticmethod
    def update(db: Session, nim: str, actor_nim: str, payload: MahasiswaUpdate) -> Mahasiswa:
        if actor_nim != nim:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update other mahasiswa")
        mahasiswa = MahasiswaController.get_by_nim(db, nim)
        if payload.email and payload.email != mahasiswa.email:
            if db.scalar(select(Mahasiswa).where(Mahasiswa.email == payload.email)):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
            mahasiswa.email = payload.email
        if payload.nama_depan is not None:
            mahasiswa.nama_depan = payload.nama_depan
        if payload.nama_belakang is not None:
            mahasiswa.nama_belakang = payload.nama_belakang
        if payload.password is not None:
            mahasiswa.password = hash_password(payload.password)
        db.commit()
        db.refresh(mahasiswa)
        return mahasiswa

    @staticmethod
    def verify_credentials(db: Session, payload: CredentialVerifyRequest) -> Mahasiswa:
        mahasiswa = db.scalar(select(Mahasiswa).where(Mahasiswa.email == payload.email))
        if not mahasiswa or not verify_password(payload.password, mahasiswa.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return mahasiswa
