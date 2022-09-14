create database banco_sensedia;

create table cad_cnpj(
	cod_cliente serial primary key,
	cnpj varchar(14) not null,
	nome_cliente varchar(255) not null,
	cidade varchar(255) not null,
	estado varchar(10) not null;
	cep varchar(8) not null;
);