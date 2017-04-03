#include <stdio.h>
#include <stdlib.h>

//

/** ElemType may be changed for application
 * specific needs.
 *
 * However, it should be a numeric type.
 */

typedef int ElemType;
#define FORMAT " %i "
#define DEFAULT 0

// hidden implementation of list_struct
typedef struct list_struct LIST;

extern LIST *lst_create(); 
extern void lst_free(LIST *l);
extern void lst_print(LIST *l); 


extern void lst_push_front(LIST *l, ElemType val); 
extern void lst_push_back(LIST *l, ElemType val); 
extern int lst_len(LIST *l);
extern int lst_is_empty(LIST *l);
extern void lst_merge_sorted(LIST *a, LIST*b);



typedef struct node {
    ElemType val;
    struct node *next;
} NODE;


struct list_struct {
    NODE *front;
    NODE *back;
};


/*
* returns pointer to newly created empty list
*/
LIST *lst_create() {
  LIST *l = malloc(sizeof(LIST));

  l->front = NULL;
  l->back = NULL;
  return l;
}

void lst_free(LIST *l) {
NODE *p = l->front;
NODE *pnext;

  while(p != NULL) {
    pnext = p->next;   // keeps us from de-referencing a freed ptr
    free(p);
    p = pnext;
  }
  // now free the LIST 
  free(l);
}

void lst_print(LIST *l) {
  NODE *p = l->front;

  printf("[");
  while(p != NULL) {
    printf(FORMAT, p->val);
    p = p->next;
  }
  printf("]\n");
  
  return;
}

/**
* TODO:  print in reverse order 
*
* Try to do without looking at notes!
* Hints:  recursive helper function
*/
void lst_rev_helper(NODE *p){
  if(p==NULL)
    return;
 lst_rev_helper(p->next);
 printf(FORMAT, p->val);
}
void lst_print_rev(LIST *l) {
  NODE *p = l->front;
  lst_rev_helper(p);
  return;
}

void lst_push_front(LIST *l, ElemType val) {
  NODE *p = malloc(sizeof(NODE));
  p->val = val;
  p->next = l->front;
  
  l->front = p;
  if(l->back == NULL)   // was empty, now one elem
    l->back = p;
  return;
}

void lst_push_back(LIST *l, ElemType val) {
  NODE *p;

  if(l->back == NULL){   // list empty - same as push_front
    lst_push_front(l, val);
    return;
  }
  else {  // at least one element before push
    p = malloc(sizeof(NODE));
    p->val = val;
    p->next = NULL;
    l->back->next = p;
    
    l->back = p;
    return;
  }
}

int lst_len(LIST *l) {
NODE *p = l->front;
int n=0;

  while(p != NULL) {
    n++;
    p = p->next;
  }
  return n;
}

int lst_is_empty(LIST *l) {
  return l->front == NULL;
}


/** TODO
 *    function:  lst_count
*     description:  Counts number of occurrences 
*     		of x in the list and returns 
*     		that value.
*/
int lst_count(LIST *l, ElemType x) {
int count = 0;
NODE *p;
if (l){
p = l->front;
while ( p != NULL)
	{
		if ( p ->val == x)
			count++;
		p=p->next;
	}
  return count; 
}
else 
	return count;

}
/* These are "sanity checker" functions that check to see
*     list invariants hold or not.
*/

int lst_sanity1(LIST *l) {
  if(l->front == NULL && l->back != NULL){
	fprintf(stderr, "lst_sanity1 error:  front NULL but back non-NULL\n");
	return 0;
  }
  if(l->back == NULL && l->front != NULL){
	fprintf(stderr, "lst_sanity1 error:  back NULL but front non-NULL\n");
	return 0;
  }
  return 1;
}

int lst_sanity2(LIST *l) {
  if(l->back != NULL && l->back->next != NULL) {
	fprintf(stderr, "lst_sanity2 error:  back elem has a non-NULL next?\n");
	return 0;
  }
  return 1;
}

/*
*   makes sure that the back pointer is also the last reachable
*    node when you start walking from front.
*    HINT:  use pointer comparison
*/
int lst_sanity3(LIST *l) {


  printf("lst_sanity3 not implemented\n");


  return 1;
}



ElemType lst_pop_front(LIST *l) {
ElemType ret;
NODE *p;
 

  if(lst_is_empty(l))
	return DEFAULT;   // no-op

  ret = l->front->val;
  
  if(l->front == l->back) {  // one element
	free(l->front);
	l->front = NULL;
	l->back = NULL;
  }
  else {
	p = l->front;  // don't lose node being deleted
	l->front = l->front->next;  // hop over
	free(p);
  }
  return ret;
}

     
  


/* TODO 
*    
*    if list is empty, we do nothing and return arbitrary value
*    otherwise, the last element in the list is removed and its
*      value is returned.
*
*/
ElemType lst_pop_back(LIST *l) {
NODE *p;
int x;
if(l){
p = l->front;
while( p != NULL){
	if (l->front== l->back){
		x=l->back->val; 
		l->front=NULL;
		free(l->front);
	return x;
	}
	if (p->next==l->back){
		x=l->back->val;  
		free(l->back);
		l->back=p;
		p->next=NULL;
		return x;
		}		
p=p->next;
}
}

	return -1; 
}
/* TODO
*  For full credit, you cannot allocate any new memory!
*
* description:  self-evident
*/
void lst_reverse(LIST *l) {
NODE *p;
NODE *q;
NODE *b;
q=NULL;
p=l->front;

while(p != NULL){
        b = p->next;
        p->next = q;
        q=p;
        p=b;
}
l->front = q;
}


/*
* removes first occurrence of x (if any).  Returns
*   0 or 1 depending on whether x was found
*/
int lst_remove_first(LIST *l, ElemType x) {
NODE *p;
NODE *tmp;

  if(l->front == NULL) return 0;
  if(l->front->val == x) {
	lst_pop_front(l);
	return 1;
  }
  // lst non-empty; no match on 1st elem
  p = l->front;

  while(p->next != NULL) {
     if(x == p->next->val) {
	tmp = p->next;
	p->next = tmp->next;
	if(tmp == l->back) 
	    l->back = p;
	free(tmp);
	return 1;
     }
     p = p->next;
  }
  return 0;
}


int lst_remove_all_slow(LIST *l, ElemType x) {
int n=0;
  while(lst_remove_first(l, x))
	n++;
  return n;
}

/** 
 * function: lst_sra_bad_case (sra:  slow_remove_all)
 *
 * description: constructs a list of length n such that 
 * the above function takes quadratic time to remove
 * all occurrences of a specified value. 
 *
 * By convention, the specified value will be 0
 */
LIST *lst_sra_bad_case(int n) {
LIST *lst;
int i;

	// idea:  first n/2 elements are non-zero
	//        the last n/2 are zeros
	//        ever call to lst_remove_first will
	//        have to walk through all of the 1's
	// [ 1 1 1 1 1 1 1 0 0 0 0 0 0 0 ]

	lst = lst_create();
	for(i=0; i<n/2; i++) 
		lst_push_front(lst, 0);
	for(i=0; i<(n-n/2); i++) 
		lst_push_front(lst, 1);
	return lst;
}


/** TODO
 * function:  lst_remove_all_fast
 * description:  same behavior as lst_remove_all_slow but has
 * 	faster execution time even on "bad cases" as generated by
 * 	the function above.  Number of operations proportional to the 
 * 	length of the list regardless of number of matches and distribution
 * 	of matches.
 *
 * Approach:  all occurrences of x removed in a single pass 
 *
 * returns: number of elements removed
*/
int lst_remove_all_fast(LIST *l, ElemType x) {
NODE *p;
int counter=0;
if (l){
p=l->front;
}
else
	return 0;
if (p->val==x){
	l->front=p->next;
	counter++;
	}
	while(p != NULL){
		if(p->next && p->next->val ==x){
			p->next=p->next->next;
			counter++;
		}
	p=p->next;
}
  printf("%i", counter);
  return counter;
}

// TODO 
int lst_is_sorted(LIST *l){
  NODE *p;
  if (l){
    p=l->front;
  }
  while( p != NULL && p->next != NULL ) {
    if (p->val > p->next->val){
      printf("0");
      return 0; 
    }
    p=p->next; 
}
  printf("1");
  return 1;

}



/** TODO
* function:  lst_insert_sorted
*
* description:  assumes given list is already in sorted order
*	   and inserts x into the appropriate position
* 	   retaining sorted-ness.
* Note 1:  duplicates are allowed.
*
* Note 2:  if given list not sorted, behavior is undefined/implementation
* 		dependent.  We blame the caller.
* 		So... you don't need to check ahead of time if it is sorted.
*/
void lst_insert_sorted(LIST *l, ElemType x) {
  NODE *y, *p;
  y=malloc(sizeof(NODE));
  y->val=x;
  if(l){
    p=l->front;
  }
  else {
    y->val=x;
    y->next=l->front;
    return;
  }
  if (x<= p->val){
    lst_push_front(l, x);
    p=p->next;
    return; 
  }
  while(p != NULL) {
    if (p->next &&  x <= p->next->val){
      y->next=p->next;
      p->next=y;
      return;
    }	
    p = p->next;
  }
  lst_push_back(l, x);
  return;
}

/** TODO
 * function:  lst_merge_sorted
 *
 * description:  assumes both list a and b are in
 * 	sorted (non-descending) order and merges them
 * 	into a single sorted list with the same
 * 	elements.  
 *
 * 	This single sorted list is stored in a while
 * 	b becomes empty.
 *
 * 	if either of given lists are not sorted, 
 * 	we blame the caller and the behavior is
 * 	implementation dependent -- i.e., don't worry
 * 	about it!
 *
 * 	Example:
 *
 * 		a:  [2 3 4 9 10 30]
 * 		b:  [5 8 8 11 20 40]
 *
 * 		after call on (a,b)
 *
 * 		a:  [2 3 4 5 8 8 9 10 11 20 30 40]
 * 		b:  []
 * 
 * implementation:  should not allocate ANY new list
 * 	nodes -- it should just re-link existing
 * 	nodes.
 *
 * 	Must be linear time in the |a|+|b| -- i.e.,
 * 	the total number of elements being processed.
 */
void lst_merge_sorted(LIST *a, LIST *b){
  printf("why\n");
  NODE *p, *q;
  int count=0;
  printf("hi");
  if(a){
    p = a->front;
  }
  else{
    p = NULL;
  }
  if(b){
    q = b->front;
  }
  else{
    q = NULL;
    return;
  }
  printf("hello");
  while (p !=NULL && q != NULL){
    while(q->val <= p->val){
      lst_push_front(a, q->val);
      b->front=NULL;
      free(b->front);
      b->front = q->next;
      q = q->next;
      count++;
    }
    printf("finished first while loop\n");
    if(p->next){
      while(q != NULL && q->val <= p->next->val){
	q->next = p->next;
	p->next = q;
	q = q->next;
	count++;
      }
    }
    printf("finished second while loop\n");
    p = p->next;
    count ++;
  }
  printf("REACHED END OF A LIST\n");
  if (b){
    if(b->front){	 
      a->back->next=b->front; 
    }
    else{
      return;
    }
    printf("seg\n");
    b->front = NULL;
    b->back = NULL;
    printf("fault\n");
    //free(b->front);
    //free(b->back);
    return;
  }
  return;
}



int main() {
  LIST *lst1 = lst_create();
  
  for(int i = 0; i < 10; i++)
    lst_push_back(lst1,i);

  LIST *lst2 = lst_create();
  for(int i = 11; i < 20; i++)
    lst_push_back(lst2,i);
  
  lst_print(lst1);
  lst_print(lst2);

  printf("segfault\n");
  lst_merge_sorted(lst1,lst2);

  lst_print(lst1);
  lst_print(lst2);
  return 0;
}

