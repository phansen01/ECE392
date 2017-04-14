#include<stdio.h>
#include<stdlib.h>

long long m[64];

/* accepts the adjacency matrix on stdin. Each row is a 
   64-bit integer in binary form: column zero is on the far right, row zero is at the top
*/
int main(int argc, char** argv) {
	char line[128];
	long long nodes=0;
	while(fgets(line,128,stdin)) {		
		m[nodes++]=strtoq(line,0,2);
	}

	for(int j=0;j<nodes*nodes;j++) {
		int jy=j/nodes;
		int jx=j%nodes;

		for(int i=nodes*nodes-1;i>=0;i--) {
			int iy=i/nodes;
			int ix=i%nodes;		

			printf("%d",((m[iy]>>jy)&1) & ((m[ix]>>jx)&1) & (i!=j));
		}
		printf("\n");
	}
}
