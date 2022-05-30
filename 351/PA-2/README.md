
In this programming assignment, your task is to create a lab entry system that will be used to keep track of students that entered our laboratories. You will use extendible hashing structure to store the students. For detailed description, please refer to 10.2 EXTENDIBLE HASHING chapter in Database Management Systems (by Raghu Ramakrishnan and Johannes Gehrke) book. Although extendible hashing in the lecture notes uses the first k bits, we will use a different flavor (the last k bits) in this assignment.

The lab entry system is summarized as follows:
	• Students enter the laboratory by showing their ID cards to our lab entrance system.
	• When a student enters the laboratory, we store his/her studentID (i.e., ”e1234567”).
	• StudentIDs are stored in extendible hashing structure.
	• When a student leaves the laboratory, we remove the related studentID from the system.
