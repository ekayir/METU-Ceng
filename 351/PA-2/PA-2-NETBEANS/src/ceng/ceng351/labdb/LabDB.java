package ceng.ceng351.labdb;

import java.util.ArrayList;

public class LabDB {

    ArrayList<Bucket> bucketList = new ArrayList<>();
    public int globalBucketSize = 0;
    public int globalDepth = 1;

    public LabDB(int bucketSize) {
        Bucket b1 = new Bucket(1, bucketSize);
        bucketList.add(b1);
        bucketList.add(new Bucket(1, bucketSize));
        this.globalBucketSize = bucketSize;
    }

    public void enter(String studentID) {
        if (search(studentID) != "-1") {
            return;
        }

        int hashValue = GetHashValue(studentID);
        Bucket bucket = bucketList.get(hashValue);
        int currentLength = bucket.StudentIds.size();
        boolean check = currentLength == globalBucketSize;
        while (check) {
            int temp_startpoint = hashValue / Power(2, globalDepth - bucket.LocalDepth)
                    * Power(2, globalDepth - bucket.LocalDepth);
            if (bucket.LocalDepth == globalDepth) {
                temp_startpoint = hashValue / 2 * 2;
            }

            if (bucket.LocalDepth == globalDepth) {
                //global split
                globalDepth++;
                ArrayList<Bucket> tempHashList = new ArrayList<Bucket>();
                int counter = 0;
                for (Bucket hashPointer : bucketList) {
                    tempHashList.add(hashPointer);
                    tempHashList.add(hashPointer);
                }
                /*for (Bucket hashPointer : bucketList) {
                 tempHashList.add(hashPointer);                    
                 }*/
                bucketList = tempHashList;
                temp_startpoint *= 2;
            }

            int temp_cond = Power(2, globalDepth - bucket.LocalDepth);

            Bucket tempBucket2 = null;
            tempBucket2 = bucketList.get(temp_startpoint);
            Bucket tempBucket = new Bucket(tempBucket2.LocalDepth + 1, globalBucketSize);
            bucketList.get(temp_startpoint).LocalDepth++;

            for (int i = 0; i < temp_cond; i++) {

                if (i < temp_cond / 2) {
                    continue;
                } else {
                    bucketList.remove(temp_startpoint);
                    bucketList.add(temp_startpoint, tempBucket);
                }
                temp_startpoint++;
            }

            int sizeOfBucket = tempBucket2.StudentIds.size();
            Bucket tempBucket10 = new Bucket(tempBucket2.LocalDepth + 1, globalBucketSize);
            for (int i = 0; i < sizeOfBucket; i++) {
                tempBucket10.StudentIds.add(tempBucket2.StudentIds.get(i));
            }
            tempBucket2.StudentIds.clear();
            for (int i = 0; i < sizeOfBucket; i++) {
                String tempBucketStudentId = tempBucket10.StudentIds.get(i);
                int newHashValue = GetHashValue(tempBucketStudentId);
                bucketList.get(newHashValue).StudentIds.add(tempBucketStudentId);
            }

            hashValue = GetHashValue(studentID);
            bucket = bucketList.get(hashValue);
            check = bucket.StudentIds.size() == globalBucketSize;
        }
        hashValue = GetHashValue(studentID);
        bucket = bucketList.get(hashValue);
        bucket.StudentIds.add(studentID);
    }

    public void leave(String studentID) {
        Boolean isDeleted = false;
        int hashValue = GetHashValue(studentID);
        Bucket bucket = bucketList.get(hashValue);
        if (bucket != null) {
            int sizeOfBucket = bucket.StudentIds.size();

            for (int j = 0; j < sizeOfBucket; j++) {
                if (bucket.StudentIds.get(j).equals(studentID) == true) {
                    bucket.StudentIds.remove(j);
                    isDeleted = true;
                    break;
                }
            }
        }

        while (isDeleted == true && globalDepth != 1 && bucket.StudentIds.size() == 0) {
            boolean isMerged = false;
            int buddyIndex = findBuddyIndex(bucket, hashValue);

            //merge
            Bucket tempBucket = bucketList.get(buddyIndex);
            if (tempBucket.LocalDepth == bucket.LocalDepth) {
                for (int i = 0; i < Power(2, (globalDepth - bucket.LocalDepth)); i++) {
                    bucketList.remove(hashValue + i);
                    bucketList.add(hashValue + i, tempBucket);
                    isMerged = true;
                }
                tempBucket.LocalDepth--;
            }

            //check halfing directories. if no, half directories
            if (isExistBucketSameGlobalPath() == false) {
                int sizeOfBucketList = bucketList.size();
                for (int i = sizeOfBucketList - 1; i > 0; i -= 2) {
                    if (i >= 0) {
                        bucketList.remove(i);
                    }
                }
                globalDepth--;
            }

            hashValue = GetHashValue(studentID);
            if (isMerged == false) {
                break;
            }
            bucket = bucketList.get(hashValue);
        }
    }

    public int findBuddyIndex(Bucket bucket, Integer index) {

        String a = "";
        String b = Integer.toString(index, 2);
        for (int i = b.length(); i < globalDepth; i++) {
            a += "0";
        }
        a += b;

        String temp = Reverse(
                GetLeftPaddedAndTruncated(bucket.LocalDepth, Reverse(a)));
        int len = temp.length();
        temp = (temp.substring(0, len - 1) + (temp.charAt(len - 1) == '0' ? '1' : '0'));

        for (int i = 0; i < globalDepth - bucket.LocalDepth; i++) {
            temp += "0";
        }

        return Integer.parseInt(temp, 2);
    }

    public String search(String studentID) {
        int hashValue = GetHashValue(studentID);
        Bucket bucket = bucketList.get(hashValue);
        if (bucket == null) {
            return "-1";
        }

        for (String studentId : bucket.StudentIds) {
            if (studentId.equals(studentID) == true) {
                return Reverse(GetLeftPaddedAndTruncated(globalDepth, Integer.toString(hashValue, 2)));
            }
        }
        return "-1";
    }

    public void printLab() {
        int i = 0;
        System.out.println("Global depth : " + globalDepth);
        int sizeOfBucket = bucketList.size();
        for (int j = 0; j < sizeOfBucket; j++) {
            String binaryNumber = Integer.toString(j, 2);
            int index = Integer.parseInt(Reverse(GetLeftPaddedAndTruncated(globalDepth, binaryNumber)), 2);
            Bucket bucket = bucketList.get(index);
            String result
                    = GetLeftPaddedAndTruncated(globalDepth, binaryNumber) + " : [Local depth:"
                    + bucket.LocalDepth + "]";
            for (String StudentId : bucket.StudentIds) {
                result += "<" + StudentId + ">";
            }
            System.out.println(result);
        }
    }

    public int GetHashValue(String studentID) {

        int studentIdNumber = Integer.parseInt(studentID.substring(1));
        String binaryNumber = Integer.toString(studentIdNumber, 2);
        return Integer.parseInt(Reverse(GetLeftPaddedAndTruncated(globalDepth, binaryNumber)), 2);
    }

    private String GetLeftPaddedAndTruncated(int length, String string) {
        String result = "";
        if (length > string.length()) {
            for (int i = string.length(); i < length; i++) {
                result += "0";
            }
            result += string;
        } else {
            result = string.substring(string.length() - length, string.length());
        }

        return result;
    }

    private String Reverse(String param) {
        return new StringBuilder(param).reverse().toString();
    }

    private int Power(int alt, int ust) {
        int result = 1;
        for (int i = 0; i < ust; i++) {
            result = result * alt;
        }
        return result;
    }

    //this method check existence of any bucket whose local depth is same global depth
    private Boolean isExistBucketSameGlobalPath() {
        for (Bucket bucket : bucketList) {
            if (bucket.LocalDepth == globalDepth) {
                return true;
            }
        }
        return false;
    }

    private int getEmptyBucketAddressWithSameGlobalDepth() {
        int sizeOfBucket = bucketList.size();
        for (int i = 0; i < sizeOfBucket; i++) {
            if (bucketList.get(i).StudentIds.size() == 0) {
                return i;
            }
        }
        return -1;
    }
}
