package ceng.ceng351.labdb;



public class LabDB {
	List<Bucket> bucketList;
    public LabDB(int bucketSize) {
        bucketList.
    }

    public void enter(String studentID) {
        
    }

    public void leave(String studentID) {
        
    }

    public String search(String studentID) {
        return "";
    }

    public void printLab() {
        
    }
}

public class Bucket
{
	public Bucket(int localDepth,int bucketSize)
	{
		this.LocalDepth = localDepth;
		this.StudentIds = new String[bucketSize];
		this.BucketSize = bucketSize;
	}
	public int LocalDepth;
	public String[] StudentIds;  	
	public int BucketSize;
}