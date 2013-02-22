SUBROUTINE STRUCTURE_READ(FILE_NAME, J2, N_ATOMS, READ_IN_COORDS)
  IMPLICIT NONE
  
      
  INTEGER :: J, K
  INTEGER, INTENT(IN) :: J2, N_ATOMS
  CHARACTER(LEN=120) :: FILE_NAME
  DOUBLE PRECISION, DIMENSION(3*N_ATOMS), INTENT(OUT) :: READ_IN_COORDS
  
  
  ! =========== OBTAIN STRUCTURAL DATA =========== !
  
   !NATOMS = 69 ! EVENTUALY WANT TO READ THIS VALUE FROM A FILE
   
  
   !J2 = 2536
   
   !ALLOCATE(READ_IN_COORDS(3*N_ATOMS))
   
   OPEN(UNIT=2,FILE=TRIM(FILE_NAME),ACCESS='DIRECT',FORM='UNFORMATTED',STATUS='OLD',RECL=8*3*N_ATOMS)
   
  
   
   !WRITE(6,*) 'I', I
   READ(2,REC=J2) (READ_IN_COORDS(J),J=1,3*N_ATOMS)
   !WRITE(6,*) 'I', I
   DO J=1, N_ATOMS
      K = 3*(J - 1)
      !WRITE(*,*) READ_IN_COORDS(K +1: K+ 3)
   ENDDO
   
   !WRITE(6,'(A)') 'Structural Data Obtained'
   CLOSE(2)
   

 END SUBROUTINE STRUCTURE_READ
