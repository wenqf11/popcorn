package cn.edu.tsinghua.thss.popcorn.utils;

import java.security.MessageDigest;

/**
 * Created by 兜哥 on 2016/7/11.
 */
public class PasswordMd5 {

    public static String md5(String username) {

            StringBuilder sb=new StringBuilder();
            try {
                MessageDigest instance = MessageDigest.getInstance("MD5");
                byte[] bytes = username.getBytes();
                byte[] digest = instance.digest(bytes);
                for(int i=0;i<digest.length;i++){
                    int i1 = digest[i] & 0xFF;//把负数转换成正数
                    String s = Integer.toHexString(i1);
                    if(s.length()<2){
                        sb.append("0");
                    }
                    sb.append(s);
                }
                return sb.toString();

            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;

    }
}
