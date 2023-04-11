truncate table chem.tmp1;
insert into chem.tmp1 
select synonyms, full_molformula,
 row_number() over(partition by full_molformula order by CHAR_LENGTH(synonyms)) as rn
from chem.COMPOUND_PROPERTIES prop
join chem.MOLECULE_SYNONYMS sym
on prop.molregno = sym.molregno
and sym.syn_type not in ('RESEARCH_CODE', 'MERCK_INDEX', 'E_NUMBER')
;

truncate table chem.tmp2;
insert into chem.tmp2
select synonyms, full_molformula 
from chem.tmp1
where rn = 1;

select * 
from chem.tmp2
INTO OUTFILE 'C:\\Users\\daniil.elizarov\\PycharmProjects\\LAb02_data_generate\\data\\chems.csv'
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n';

