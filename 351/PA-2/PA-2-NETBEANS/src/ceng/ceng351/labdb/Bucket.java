/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ceng.ceng351.labdb;

import java.util.ArrayList;

/**
 *
 * @author Software
 */
public class Bucket {
    
     public Bucket(int localDepth, int bucketSize) {
        this.LocalDepth = localDepth;
        this.StudentIds = new ArrayList<String>();
        this.BucketSize = bucketSize;
    }
    
    public int LocalDepth;
    public ArrayList<String> StudentIds;
    public int BucketSize;
}
