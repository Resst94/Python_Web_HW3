Task #3

The first part is for threads

Write a program to process the "Junk" folder that sorts the files in the specified folder by extension using several threads. Speed up the processing of large directories with a large number of subfolders and files by parallelizing the traversal of all folders in separate threads. The most time-consuming task will be to transfer a file and get a list of files in the folder (iterating through the contents of the directory). To speed up file transfer, you can perform it in a separate thread or thread pool. This is all the more convenient because you don't process the result of this operation in the application and you don't need to collect any results. To speed up the traversal of the contents of a directory with multiple nesting levels, you can process each subdirectory in a separate thread or pass the processing to a thread pool.

The second part is for processes

Write an implementation of the factorize function that takes a list of numbers and returns a list of numbers by which the numbers in the input list are divided without remainder.

Implement a synchronous version and measure the execution time.

Then, improve the performance of your function by implementing the use of multiple processor cores for parallel computation and measure the execution time again. To determine the number of cores on your machine, use the cpu_count() function from the multiprocessing package.
