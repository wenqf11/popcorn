package cn.edu.tsinghua.thss.popcorn.utils;

import android.widget.Toast;
import android.content.Context;
/**
 * Created by vince on 2016-11-01.
 */
public class NoRepeatToast {
    private static Toast mToast = null;
    public static void showToast(Context context, String text, int duration) {
        if (mToast == null) {
            mToast = Toast.makeText(context, text, duration);
        } else {
            mToast.setText(text);
            mToast.setDuration(duration);
        }

        mToast.show();
    }
}
