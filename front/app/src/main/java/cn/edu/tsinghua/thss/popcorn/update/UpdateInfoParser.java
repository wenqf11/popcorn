package cn.edu.tsinghua.thss.popcorn.update;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import org.xmlpull.v1.XmlPullParser;

import android.util.Xml;

import cn.edu.tsinghua.thss.popcorn.AboutInfoActivity;
import cn.edu.tsinghua.thss.popcorn.config.Config;

/**
 * Created by vince on 2015/7/17.
 */
public class UpdateInfoParser {
    public static UpdateInfo getUpdataInfo(InputStream is) throws Exception{
        XmlPullParser  parser = Xml.newPullParser();
        parser.setInput(is, "utf-8");
        int type = parser.getEventType();
        UpdateInfo info = new UpdateInfo();
        while(type != XmlPullParser.END_DOCUMENT ){
            switch (type) {
                case XmlPullParser.START_TAG:
                    if("version".equals(parser.getName())){
                        info.setVersion(parser.nextText());
                    }else if ("url".equals(parser.getName())){
                        info.setUrl(parser.nextText());
                    }else if ("description".equals(parser.getName())){
                        info.setDescription(parser.nextText());
                    }
                    break;
            }
            type = parser.next();
        }
        return info;
    }

    public static String getRemoteVersion(){
        try {
            InputStream is = null;
            UpdateInfo info;
            URL url = new URL(Config.VERSION_SERVER_URL);
            HttpURLConnection conn = (HttpURLConnection) url
                    .openConnection();
            conn.setConnectTimeout(5000);
            int responseCode = conn.getResponseCode();
            if (responseCode == 200) {
                // 从服务器获得一个输入流
                is = conn.getInputStream();
            }
            info = UpdateInfoParser.getUpdataInfo(is);
            return info.getVersion();
        }catch (Exception e) {
            e.printStackTrace();
        }
        return "";
    }
}
