package cn.edu.tsinghua.thss.popcorn.update;
import java.io.InputStream;
import org.xmlpull.v1.XmlPullParser;
import android.util.Xml;

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
}