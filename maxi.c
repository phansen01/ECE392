#include<stdio.h>
#include<stdlib.h>

unsigned long long m[64]={0};

/* returns the size of the independent set, or zero if not independent */
int independent(unsigned long long set, int nodes) {
	int set_size=0;
	unsigned long long neighbors = 0;
	
	for(int i=0;i<nodes;i++) {
		if((set>>i)&1) {
			set_size++;
			neighbors |= m[i];
		}
	}

	// if the intersection of the union and the neighbors is zero, the set is independent.
	// return the size of the set
	if(!(neighbors & set)) return set_size;
	else return 0;		 
}

/* prints in binary integer order - node zero is at the right */
void printset(unsigned long long set, int nodes) {
	for(int i=nodes-1;i>=0;i--) {
		printf("%lld",(set>>i)&1);
	}
	printf("\n");
}


/* returns the size of the independent set, or zero if not independent */

/* accepts the adjacency matrix on stdin. Each row is a 
   64-bit integer in binary form: column zero is on the far right, row zero is at the top
*/
int main(int argc, char** argv) {
	char line[128];
	long long nodes=0;

	/* read in the graph adjacency matrix */
	while(fgets(line,128,stdin)) {		
		m[nodes++]=strtoq(line,0,2);
	}

	/* run the algorithm twice: 
		  once to find the size of the max set, 
		  once to output all sets of that size
	*/

	// find max independent set size
	int maxsize = 0;
	for(unsigned long long i=0; i < (1<<nodes); i++) {
		int result = independent(i,nodes);
		if(result > maxsize) {
			maxsize = result;
		}
	}
	printf("Max independent set size is %d\n",maxsize);


	// output all sets of the max size
	for(unsigned long long i=0; i < (1<<nodes); i++) {
		int result = independent(i,nodes);
		if(result == maxsize) {			
			printset(i, nodes);
		}
	}

}
