
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <pthread.h>


uint8_t sickle_cell[] = { 1, 1, 1, 2, 0, 1, 2 }; 

/* Cheak for variences that are the same as the expression. */  
inline int check_line(char * line, size_t format_loc, size_t family_num){
    char tokline[strlen(line)+1];
    strcpy(tokline, line);
    
    char *sp=tokline, *gt, *st=tokline; //Strtok
    size_t i;
    uint8_t family[family_num];//Array of gtsums one for each family member
    
    for(i=0; i<=format_loc; i++){
      st = strtok_r(NULL, " \t", &sp);
    }
    
    for(i=0; i<family_num; i++){
      st = strtok_r(NULL, " \t", &sp);
      gt=st;
      st = strtok_r(NULL, ":", &gt);
      family[i] = (st[0]=='1') + (st[2]=='1');
      //fprintf(stderr,"%u, %s,%u,%u\n", family[i], st, st[0]=='1', st[2]=='1');
    }

    //check for possible mutations that match expression
    size_t m=0;
    for(i=0; i<family_num; i++){
      m += (sickle_cell[i]==family[i]);
      //printf("%u&%u ", family[i], sickle_cell[i]);
    }
    //printf("\t%u\n", m);
    
    if(m==family_num){
      printf("%s",line);
    }
    
    return 0;
}

int main(int argc, char ** argv){

    if(argc!=2){
      printf("Usage: %s .vcf|vcf.gz\n", argv[0]);
    }

    /* TODO:  popen pigz */
    
    FILE * varfile = fopen(argv[1], "r");
    if(!varfile){
      fprintf(stderr, "Couldnt open file: %s\n", argv[1]);
      exit(1);
    }

    char line[4096];
    line[1]='#';//prime

    //Skip all the lines starting with '#'
    while (fgets(line, sizeof(line)-1, varfile) != NULL && line[1]=='#');
    printf("%s",line); //Header
    
    char *sp=line, *st=NULL; //prime Strtok
    size_t idx=0, format_loc=0, family_num=0;

    /* Scan this line and find the family names and locations */
    while((st = strtok_r(NULL, " \t", &sp)) != NULL ){
      if(strcmp(st, "FORMAT")==0)format_loc=idx;
      idx++;
    }
    idx--;
    family_num=idx-format_loc;
    fprintf(stderr,"%u Family members\n", family_num);

    /* Start Checking Vareations */
    /* each line could be done in parrallel */
    while (fgets(line, sizeof(line)-1, varfile) != NULL){
      
      //No Sex Chromosomes 
      if(line[0]=='X' || line[0]=='Y') continue;
      check_line(line, format_loc, family_num);
    }
}
