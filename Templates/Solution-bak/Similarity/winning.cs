using System;

public class Program {
  public static int Puzzle(int[] a) {
	 int min=a[0],max=a[0];
	 int i=0,k=0;
		 while((i+1)!=a.Length)
		 {
			
		  if(a[i+1]>max) max = a[i+1];
		//  else max=a[i];
		  i++;
		 }
		 
		  while((k+1)!=a.Length)
		 {
		  if(a[k+1]<min) min = a[k+1];
		  //else min=a[k];
		  k++;
		 }
	  
	 
    return max-min;
  }
}