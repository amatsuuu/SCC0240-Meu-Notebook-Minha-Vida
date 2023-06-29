-- Liste o nome, ano escolar de todos os alunos que cursaram todos os cursos dados pelo coordenador ‘Jony’
SELECT A.nome, A.ano_escolar FROM ALUNO A
	WHERE NOT EXISTS (
	SELECT C.LINGUAGEM, C.ANO, C.SEMESTRE FROM CURSO AS C JOIN COORDENADOR AS CO ON C.COORDENADOR =  CO.CPF WHERE CO.NOME = ‘Jony’
	MINUS
	SELECT C.LINGUAGEM, C.ANO, C.SEMESTRE FROM ALUNO_PERT_TURMA AT JOIN TURMA T ON A.TURMA = T.ID AND AT.ALUNO = A.CPF
JOIN CURSO C ON C.LINGUAGEM = T.LINGUAGEM AND C.ANO = T.ANO AND C.SEMESTRE = T.SEMESTRE
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




-- Liste todas as escolas que não possuem aluno com dispositivos emprestados da empresa ‘Comércio e Simões EFG’.
