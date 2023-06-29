-- Liste o nome, ano escolar de todos os alunos que cursaram todos os cursos dados pelo coordenador ‘Jony’
SELECT A.nome, A.ano_escolar, A.grau_ensino FROM ALUNO A
	WHERE NOT EXISTS (
	SELECT C.LINGUAGEM, C.ANO, C.SEMESTRE FROM CURSO C JOIN COORDENADOR CO ON C.COORDENADOR =  CO.CPF WHERE CO.NOME = 'ANA OLIVEIRA'
	MINUS
	SELECT CS.LINGUAGEM, CS.ANO, CS.SEMESTRE FROM ALUNO_PERT_TURMA APT JOIN TURMA T ON APT.ID = T.ID AND APT.ALUNO = A.CPF
    JOIN CURSO CS ON CS.LINGUAGEM = T.LINGUAGEM AND CS.ANO = T.ANO AND CS.SEMESTRE = T.SEMESTRE
);



-- Liste em ordem decrescente a razão de manutenções por número de empréstimos dos modelos de dispositivos agrupados por tipo.
SELECT D.TIPO AS TIPO_DISPOSITIVO, D.MODELO AS MODELO_DISPOSITIVO, 
COUNT(M.DISPOSITIVO) / COUNT(E.DISPOSITIVO) AS RAZAO_MANUT_EMPRESTIMO
FROM DISPOSITIVO D
LEFT JOIN MANUTENCAO M ON D.NUMERO_SERIAL = M.DISPOSITIVO
LEFT JOIN EMPRESTIMO E ON E.NUMERO_SERIAL = E.DISPOSITIVO
GROUP BY D.TIPO, D.MODELO
ORDER BY RAZAO_MANUT_EMPRESTIMO DESC;


-- Qual a porcentagem de acertos dos exercícios por oferecimento do curso de ‘Python’ e ‘Javascript’.
SELECT C.linguagem, C.ano, C.semestre
			WHERE C.linguagem = ‘Python’ OR C.linguagem = ‘Javascript’
 GROUP BY C.linguagem, C.ano, C.semestre
--...



-- Liste todos os monitores e para aqueles que deram monitoria em 2021 especifique a porcentagem de alunos que realizaram empréstimos neste ano.
SELECT M.NOME, M.CPF, COUNT(E.ALUNO) / COUNT(*) AS PORCENTAGEM_EMPRESTIMO
    FROM MONITOR M
	LEFT JOIN MONITORIA MTRA
	ON M.CPF = MTRA.MONITOR
    JOIN TURMA T
    ON MTRA.TURMA = T.ID
    JOIN ALUNO_PERT_TURMA APT
	ON T.ID = APT.ID
    LEFT JOIN EMPRESTIMO E
	ON APT.ALUNO = E.ALUNO
    WHERE T.ANO = 2019
    GROUP BY M.NOME, M.CPF;



-- Liste todas as escolas que não possuem aluno com dispositivos emprestados da empresa ‘Comércio e Simões EFG’.
