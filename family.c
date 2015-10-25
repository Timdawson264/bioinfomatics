
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <pthread.h>

#define NUM_FAMILY 7
#define FORMAT_LOC 8


uint8_t sickle_cell_inheritance[] = { 1, 1, 1, 2, 0, 1, 2 };

uint8_t ssd_inheritance_ptn[]	= { 1, 1, 0, 2, 0, 2, 0 }; 
uint8_t ssd_inheritance_ptn_2[]	= { 1, 1, 1, 2, 1, 2, 1 }; 

uint8_t spp_inheritance_ptn1[] = {1, 0, 1, 0, 1, 0, 1};
uint8_t spp_inheritance_ptn2[] = {2, 1, 2, 1, 2, 0, 2};


//(1 or 2) or 3
uint8_t retina_inheritance_ptn1[] = {2, 1, 0, 2, 0, 0, 2}; 
uint8_t retina_inheritance_ptn2[] = {2, 1, 1, 2, 1, 1, 2};
uint8_t retina_inheritance_ptn3[] = {1, 0, 0, 1, 0, 0, 1};

size_t linenum;


void (*disease_check)(uint8_t family[NUM_FAMILY], char * line) = NULL;


void retina_check(uint8_t family[NUM_FAMILY], char * line){
    //check for possible mutations that match expression
    size_t m1=0,m2=0,i;

    for(i=0; i<NUM_FAMILY; i++){
        m1 += (retina_inheritance_ptn1[i] == family[i]) || (retina_inheritance_ptn2[i] == family[i]);
        m2 += (retina_inheritance_ptn3[i] == family[i]);
    }
        
    if(m1==NUM_FAMILY || m2==NUM_FAMILY){
      printf("%s",line);
    }
    
}


void spp_check(uint8_t family[NUM_FAMILY], char * line){
    //check for possible mutations that match expression
    size_t m1=0,m2=0,i;

    for(i=0; i<NUM_FAMILY; i++){
        m1 += (spp_inheritance_ptn1[i] == family[i]);
        m2 += (spp_inheritance_ptn2[i] == family[i]);
    }
        
    if(m1==NUM_FAMILY || m2==NUM_FAMILY){
      printf("%s",line);
    }
    
}

void ssd_check(uint8_t family[NUM_FAMILY], char * line){
    //check for possible mutations that match expression
    size_t m=0,i;

    for(i=0; i<NUM_FAMILY; i++){
        m += (ssd_inheritance_ptn[i]==family[i] || ssd_inheritance_ptn_2[i] == family[i]);
    }
        
    if(m==NUM_FAMILY){
      printf("%s",line);
    }
    
}


void sickle_check(uint8_t family[NUM_FAMILY], char * line){
    //check for possible mutations that match expression
    size_t m=0,i;

    for(i=0; i<NUM_FAMILY; i++){
      m += (sickle_cell_inheritance[i]==family[i]);
    }
    
    if(m==NUM_FAMILY){
      printf("%s",line);
    }
    
}

/* Calculate the inheritance pattern */  
int check_line(char * line){
    char tokline[strlen(line)+1];
    strcpy(tokline, line);
    
    char *sp=tokline, *gt, *st=tokline; //Strtok
    size_t i;
    uint8_t family[NUM_FAMILY];//Array of gtsums one for each family member
    
    for(i=0; i<=FORMAT_LOC; i++){
      st = strtok_r(NULL, " \t", &sp); //skip format_loc tokens
    }

    for(i=0; i<NUM_FAMILY; i++){ 
      st = strtok_r(NULL, " \t", &sp);
      gt=st;
      st = strtok_r(NULL, ":", &gt);
      //if(!st) fprintf(stderr, "\n\n%s\n\n", line);
      family[i] = (st[0]=='1') + (st[2]=='1');
    }
    
    disease_check(family, line);
    
    return 0;
}

int main(int argc, char ** argv){
    linenum=0;
    
    if(argc!=3){
      printf("Usage: %s (sickle|ssd|spp|retina)  .vcf\n", argv[0]);
      printf("\t sickle = Sickle Cell Anemia\n");
      printf("\t ssd =  Severe Skeletal Dysplasia\n");
      printf("\t spp =  Spastic Paraplegia\n");
      printf("\t retina = Retinitis Pigmentosa\n");
      exit(2);
    }

    if(strcmp("sickle", argv[1])==0) disease_check=sickle_check;
    if(strcmp("ssd", argv[1])==0) disease_check=ssd_check; 
    if(strcmp("spp", argv[1])==0) disease_check=spp_check;
    if(strcmp("retina", argv[1])==0) disease_check=retina_check;
    
    FILE * varfile = fopen(argv[2], "r");
    if(!varfile){
      fprintf(stderr, "Couldnt open file: %s\n", argv[2]);
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
    fprintf(stderr,"%u Family members, loc: %u\n", family_num, format_loc);

    /* Start Checking Variations */
    /* each line could be done in parrallel */
    while (fgets(line, sizeof(line)-1, varfile) != NULL){      
      //No Sex Chromosomes 
      if(line[0]=='X' || line[0]=='Y') break;
      check_line(line);
      linenum++;
    }

    fflush(stdout);
}
