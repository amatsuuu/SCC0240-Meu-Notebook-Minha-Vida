CREATE TABLE EMPRESA (
    CNPJ CHAR(18) NOT NULL,
    NOME VARCHAR2(55) NOT NULL,
    RUA VARCHAR2(50) NOT NULL,
    NUMERO NUMBER(5),
    CEP CHAR(9) NOT NULL,
    CONSTRAINT PK_EMPRESA PRIMARY KEY(CNPJ),
    CONSTRAINT CK_EMPRESA_CPNJ CHECK(REGEXP_LIKE(CNPJ, '^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$')),
    CONSTRAINT CK_EMPRESA_RUA_NUMERO CHECK(NUMERO >= 0),
    CONSTRAINT CK_EMPRESA_CEP CHECK(REGEXP_LIKE(CEP,'^\d{5}-\d{3}$'))
);

CREATE TABLE COORDENADOR(
    CPF CHAR(14) NOT NULL,
    NOME VARCHAR2(50) NOT NULL,
    DATA_NASC DATE NOT NULL,
    RUA VARCHAR2(50) NOT NULL,
    NUMERO NUMBER(5),
    CEP CHAR(9) NOT NULL,
    CONSTRAINT CK_COORDENADOR_CPF CHECK(REGEXP_LIKE(CPF, '[0-9]{3}\.[0-9]{3}\.[0-9]{3}\-[0-9]{2}')),
    CONSTRAINT PK_COORDENADOR PRIMARY KEY(CPF),
    CONSTRAINT CK_COORDENADOR_RUA_NUMERO CHECK(NUMERO >= 0),
    CONSTRAINT CK_COORDENADOR_CEP CHECK(REGEXP_LIKE(CEP,'^\d{5}-\d{3}$'))
);

CREATE TABLE MONITOR(
    CPF CHAR(14)NOT NULL,
    NOME VARCHAR2(50) NOT NULL,
    DATA_NASC DATE NOT NULL,
    RUA VARCHAR2(50) NOT NULL,
    NUMERO NUMBER(5),
    CEP CHAR(9) NOT NULL,
    CONSTRAINT PK_MONITOR PRIMARY KEY(CPF),
    CONSTRAINT CK_MONITOR_CPF CHECK(REGEXP_LIKE(CPF, '[0-9]{3}\.[0-9]{3}\.[0-9]{3}\-[0-9]{2}')),
    CONSTRAINT CK_MONITOR_RUA_NUMERO CHECK(NUMERO >= 0),
    CONSTRAINT CK_MONITOR_CEP CHECK(REGEXP_LIKE(CEP,'^\d{5}-\d{3}$'))
);

CREATE TABLE ESCOLA_PARCEIRA(
    CODIGO_INEP NUMBER(8) NOT NULL,
    NOME VARCHAR2(50) NOT NULL,
    RUA VARCHAR2(50) NOT NULL,
    NUMERO NUMBER(5),
    CEP CHAR(9) NOT NULL,
    CONSTRAINT PK_ESCOLA_PARCEIRA PRIMARY KEY(CODIGO_INEP),
    CONSTRAINT CK_ESCOLA_PARCEIRA_CD_INEP CHECK(CODIGO_INEP > 0),
    CONSTRAINT CK_ESCOLA_PARCEIRA_RUA_NUMERO CHECK(NUMERO > 0),
    CONSTRAINT CK_ESCOLA_PARCEIRA_CEP CHECK(REGEXP_LIKE(CEP,'^\d{5}-\d{3}$'))
);

CREATE TABLE SALA (
    BLOCO NUMBER(1) NOT NULL,
    ANDAR NUMBER(1) NOT NULL,
    NUMERO NUMBER(2) NOT NULL,

    CONSTRAINT PK_SALA   PRIMARY KEY (BLOCO, ANDAR, NUMERO),
    CONSTRAINT CK_BLOCO  CHECK (BLOCO BETWEEN 1 AND 8),
    CONSTRAINT CK_ANDAR  CHECK (ANDAR BETWEEN 0 AND 3),
    CONSTRAINT CK_NUMERO CHECK (NUMERO BETWEEN 1 AND 3)
);

CREATE TABLE CURSO(
    LINGUAGEM VARCHAR2(20) NOT NULL,
    ANO NUMBER(4) NOT NULL,
    SEMESTRE CHAR(1) NOT NULL,
    ANDAMENTO CHAR(1) NOT NULL,
    COORDENADOR CHAR(14) NOT NULL,
    CONSTRAINT PK_CURSO PRIMARY KEY (LINGUAGEM, ANO, SEMESTRE),
    CONSTRAINT FK_CURSO_COORDENADOR FOREIGN KEY (COORDENADOR) REFERENCES COORDENADOR(CPF),
    CONSTRAINT CK_LINGUAGEM CHECK (UPPER(LINGUAGEM) IN ('PYTHON', 'JAVASCRIPT', 'HTML', 'HTML/CSS', 'C', 'C/C++', 'C#', 'JAVA', 'TYPESCRIPT', 'R', 'SQL', 'PHP')),
    CONSTRAINT CK_SEMESTRE CHECK (SEMESTRE IN ('1', '2')),
    CONSTRAINT CK_CURSO_ANDAMENTO CHECK (UPPER(ANDAMENTO) IN ('S' , 'N'))
);

CREATE TABLE TURMA (
    ID NUMBER(4) NOT NULL,
    LINGUAGEM VARCHAR2(20) NOT NULL,
    ANO NUMBER(4) NOT NULL,
    SEMESTRE CHAR(1) NOT NULL,
    NUMERO_TURMA NUMBER(1) NOT NULL,
    QTD_ALUNOS NUMBER(2),
    BLOCO  NUMBER(1) NOT NULL,
    ANDAR  NUMBER(1) NOT NULL,
    NUMERO NUMBER(2) NOT NULL,

    CONSTRAINT PK_TURMA PRIMARY KEY (ID),
    CONSTRAINT FK1_TURMA FOREIGN KEY (BLOCO, ANDAR, NUMERO) REFERENCES SALA(BLOCO, ANDAR, NUMERO) ON DELETE CASCADE,
    CONSTRAINT UC_TURMA UNIQUE (LINGUAGEM, ANO, SEMESTRE, NUMERO_TURMA),
    CONSTRAINT CK_NUMERO_TURMA CHECK (NUMERO_TURMA > 0),
    CONSTRAINT CK_QTD_ALUNOS CHECK (QTD_ALUNOS > 0)
);

CREATE TABLE ALUNO(
    CPF CHAR(14) NOT NULL,
    REG_ALUNO CHAR(14) NOT NULL,
    ANO_ESCOLAR NUMBER(1) NOT NULL,
    GRAU_ENSINO CHAR(1) NOT NULL,
    NOME VARCHAR2(50) NOT NULL,
    DATA_NASC DATE NOT NULL,
    RUA VARCHAR2(50) NOT NULL,
    NUMERO NUMBER(5),
    CEP CHAR(9) NOT NULL,
    TURMA_ATUAL NUMBER(4),
    ESCOLA NUMBER(8) NOT NULL,
    CONSTRAINT PK_ALUNO PRIMARY KEY(CPF),
    CONSTRAINT CK_ALUNO_CPF CHECK(REGEXP_LIKE(CPF, '[0-9]{3}\.[0-9]{3}\.[0-9]{3}\-[0-9]{2}')),
    CONSTRAINT CK_ALUNO_GRAU_ENSINO CHECK(UPPER(GRAU_ENSINO) IN ('F', 'M')),
    CONSTRAINT UC_REG_ALUNO UNIQUE(REG_ALUNO,ESCOLA),
    CONSTRAINT CK_ALUNO_RUA_NUMERO CHECK(NUMERO >= 0),
    CONSTRAINT CK_ALUNO_CEP CHECK(REGEXP_LIKE(CEP,'^\d{5}-\d{3}$')),
    CONSTRAINT FK_ALUNO_TURMA FOREIGN KEY (TURMA_ATUAL) REFERENCES TURMA(ID) ON DELETE SET NULL,
    CONSTRAINT FK_ALUNO_ESCOLA FOREIGN KEY (ESCOLA) REFERENCES ESCOLA_PARCEIRA(CODIGO_INEP)
);

CREATE TABLE DISPOSITIVO(
    NUMERO_SERIAL VARCHAR2(12) NOT NULL,
    TIPO VARCHAR2(8),
    MODELO VARCHAR2(10),
    STATUS CHAR(15),
    QTD_MANUTENCAO NUMBER(2) DEFAULT 0,
    EMPRESA CHAR(18),
    CONSTRAINT PK_DISPOSITIVO PRIMARY KEY (NUMERO_SERIAL),
    CONSTRAINT FK_DISPOSITIVO_EMPRESA FOREIGN KEY (EMPRESA) REFERENCES EMPRESA(CNPJ) ON DELETE SET NULL,
    CONSTRAINT CK_STATUS CHECK(UPPER(STATUS) IN ('EMPRESTADO', 'EM MANUTENCAO', 'DISPONIVEL', 'EXTRAVIADO' , 'FORA DE SERVICO')),
    CONSTRAINT CK_QTD_MANUTENCAO CHECK(QTD_MANUTENCAO >= 0)
);
  
CREATE TABLE TRANSACAO(
    EMPRESA CHAR(18) NOT NULL,
    COORDENADOR CHAR(14) NOT NULL,
    DATA DATE NOT NULL,
    CONTA_DESTINO NUMBER(12) NOT NULL,
    CONTA_ORIGEM NUMBER(12) NOT NULL,
    VALOR NUMBER(10,2) NOT NULL,
    ID_TRANSACAO VARCHAR2(20) NOT NULL,
    CONSTRAINT PK_TRANSACAO PRIMARY KEY (EMPRESA, COORDENADOR, DATA),
    CONSTRAINT FK_TRANSACAO_COODENADOR FOREIGN KEY (COORDENADOR) REFERENCES COORDENADOR(CPF),
    CONSTRAINT FK_TRANSACAO_EMPRESA FOREIGN KEY (EMPRESA) REFERENCES EMPRESA(CNPJ),
    CONSTRAINT UC_ID_TRANSACAO UNIQUE (ID_TRANSACAO),
    CONSTRAINT CK_VALOR CHECK(VALOR > 0),
    CONSTRAINT CK_DATA CHECK(TO_CHAR(DATA, 'DD-MM-YYYY') > '01-01-2000'),
    CONSTRAINT CK_CONTA CHECK(CONTA_ORIGEM > 0 AND CONTA_DESTINO > 0)
);

CREATE TABLE EMPRESTIMO (
    DISPOSITIVO VARCHAR2(12) NOT NULL,
    ALUNO CHAR(14) NOT NULL,
    DATA DATE NOT NULL,
    DATA_DEVOLUCAO DATE NOT NULL,
    CONSTRAINT PK_EMPRESTIMO PRIMARY KEY (DISPOSITIVO, ALUNO, DATA),
    CONSTRAINT FK_EMPRESTIMO_DISPOSITIVO FOREIGN KEY (DISPOSITIVO) REFERENCES DISPOSITIVO(NUMERO_SERIAL),
    CONSTRAINT FK_EMPRESTIMO_ALUNO FOREIGN KEY (ALUNO) REFERENCES ALUNO(CPF),
    CONSTRAINT CK_EMPRESTIMO_DATA CHECK(DATA_DEVOLUCAO > DATA)
);

CREATE TABLE MANUTENCAO(
    DATA DATE NOT NULL,
    DISPOSITIVO VARCHAR2(12) NOT NULL,
    NOME_DO_TECNICO VARCHAR2(50) NOT NULL,
    CONSTRAINT PK_MANUTENCAO PRIMARY KEY (DATA, DISPOSITIVO),
    CONSTRAINT FK_MANUTENCAO_DISPOSITIVO FOREIGN KEY (DISPOSITIVO) REFERENCES DISPOSITIVO(NUMERO_SERIAL)
);

CREATE TABLE ALUNO_PERT_TURMA (
    ID NUMBER(4) NOT NULL,
    ALUNO CHAR(14) NOT NULL,

    CONSTRAINT PK_ALUNO_PERT_TURMA PRIMARY KEY (ID, ALUNO),
    CONSTRAINT FK1_ALUNO_PERT_TURMA FOREIGN KEY (ID) REFERENCES TURMA(ID) ON DELETE CASCADE,
    CONSTRAINT FK2_ALUNO_PERT_TURMA FOREIGN KEY (ALUNO) REFERENCES ALUNO(CPF) ON DELETE CASCADE
);

CREATE TABLE AULA (
    TURMA NUMBER(4) NOT NULL,
    DATA DATE NOT NULL,
    DIA_SEMANA VARCHAR2(7),
    HORA VARCHAR2(5),
    TEMA VARCHAR2(40),
    DESCRICAO VARCHAR2(80),

    CONSTRAINT PK_AULA  PRIMARY KEY (TURMA, DATA),
    CONSTRAINT FK1_AULA FOREIGN KEY (TURMA) REFERENCES TURMA(ID) ON DELETE CASCADE,
    CONSTRAINT CK_DIA_SEMANA CHECK (UPPER(DIA_SEMANA) IN ('SEGUNDA', 'TERCA', 'QUARTA', 'QUINTA', 'SEXTA', 'SABADO', 'DOMINGO')),
    CONSTRAINT CK_HORA CHECK (REGEXP_LIKE(HORA, '[:digit:]{1,2}\:[:digit:]{1,2}'))
);

-- Trigger para inser��o autom�tica do ID
CREATE SEQUENCE id_turma
    START WITH 1;

CREATE OR REPLACE TRIGGER incremento
    BEFORE INSERT ON TURMA
    FOR EACH ROW
BEGIN
    SELECT id_turma.NEXTVAL
    INTO :new.ID
    FROM DUAL;
END;
/

CREATE TABLE FREQUENCIA(
    ALUNO CHAR(14) NOT NULL,
    TURMA NUMBER(1) NOT NULL,
    DATA_AULA DATE NOT NULL,

    CONSTRAINT FK_FREQUENCIA_ALUNO FOREIGN KEY (ALUNO) REFERENCES ALUNO(CPF) ON DELETE CASCADE,
    CONSTRAINT FK_FREQUENCIA_AULA FOREIGN KEY (TURMA, DATA_AULA) REFERENCES AULA(TURMA, DATA) ON DELETE CASCADE,
    CONSTRAINT PK_FREQUENCIA PRIMARY KEY(ALUNO, TURMA, DATA_AULA)
);

CREATE TABLE EXERCICIO(
    TURMA NUMBER(4) NOT NULL,
    DATA_AULA DATE NOT NULL,
    NUMERO NUMBER(2) NOT NULL,
    DESCRICAO VARCHAR2(255),
    GABARITO CHAR(1) NOT NULL,
    DATA_ENTREGA DATE NOT NULL,

    CONSTRAINT CK_EXERCICIO CHECK(UPPER(GABARITO) IN ('A', 'B', 'C', 'D', 'E')),
    CONSTRAINT FK_EXERCICIO_AULA FOREIGN KEY (TURMA, DATA_AULA) REFERENCES AULA(TURMA, DATA) ON DELETE CASCADE,
    CONSTRAINT PK_EXERCICIO PRIMARY KEY(TURMA, DATA_AULA, NUMERO)
);

CREATE TABLE RESPOSTA(
    ALUNO CHAR(14) NOT NULL,
    TURMA NUMBER(4) NOT NULL,
    DATA_AULA DATE NOT NULL,
    EXERCICIO NUMBER(2) NOT NULL,
    ALTERNATIVA CHAR(1) NOT NULL,
    DATA_SUBMISSAO DATE NOT NULL,
    COMENTARIO VARCHAR2(255),

    CONSTRAINT CK_RESPOSTA CHECK(UPPER(ALTERNATIVA) IN ('A', 'B', 'C', 'D', 'E')),
    CONSTRAINT FK_RESPOSTA_EXERCICIO FOREIGN KEY (TURMA, DATA_AULA, EXERCICIO) REFERENCES EXERCICIO(TURMA, DATA_AULA, NUMERO) ON DELETE CASCADE,
    CONSTRAINT FK_RESPOSTA_ALUNO FOREIGN KEY (ALUNO) REFERENCES ALUNO(CPF) ON DELETE CASCADE,
    CONSTRAINT PK_RESPOSTA PRIMARY KEY (ALUNO, TURMA, DATA_AULA, EXERCICIO)
);

CREATE TABLE MONITORIA(
    TURMA NUMBER(4) NOT NULL,
    MONITOR CHAR(14) NOT NULL,

    CONSTRAINT FK_MONITORIA_TURMA FOREIGN KEY (TURMA) REFERENCES TURMA(ID) ON DELETE CASCADE,
    CONSTRAINT FK_MONITORIA_MONITOR FOREIGN KEY (MONITOR) REFERENCES MONITOR(CPF) ON DELETE CASCADE,
    CONSTRAINT PK_MONITORIA PRIMARY KEY (TURMA, MONITOR)
);
