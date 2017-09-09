package cn.edu.tsinghua.thss.popcorn;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.media.RingtoneManager;
import android.net.Uri;
import android.support.v4.app.NotificationCompat;
import android.util.Log;
import android.widget.Toast;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;

import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.utils.SharedPreferencesUtil;

/**
 * Created by vince on 2015/8/18.
 */
public class AlarmReceiver extends BroadcastReceiver {
    private MediaPlayer mMediaPlayer;

    public static int PlaySound(final Context context, int vibrateDuration) {
        NotificationManager mgr = (NotificationManager) context
                .getSystemService(Context.NOTIFICATION_SERVICE);
        NotificationCompat.Builder mBuilder = new NotificationCompat.Builder(context);
        mBuilder.setContentTitle("您有新的任务未完成！")
                .setWhen(System.currentTimeMillis())//通知产生的时间，会在通知信息里显示，一般是系统获取到的时间
                .setTicker("新任务通知来啦") //通知首次出现在通知栏，带上升动画效果的
                .setContentIntent(getDefalutIntent(context, Notification.FLAG_AUTO_CANCEL)) //设置通知栏点击意图
                .setPriority(Notification.PRIORITY_DEFAULT) //设置该通知优先级
                .setSmallIcon(R.drawable.ic_launcher);//设置通知小ICON
        Notification nt = mBuilder.build();
        nt.defaults = Notification.DEFAULT_SOUND;
        nt.flags |= Notification.FLAG_AUTO_CANCEL;
        if (vibrateDuration != 0) {
            ArrayList<Integer> vibrateArray = new ArrayList<Integer>();
            vibrateArray.add(0);

            for(int i = 0; i < vibrateDuration; ++i){
                vibrateArray.add(700);
                vibrateArray.add(300);
            }
            long[] vibrate = new long[vibrateArray.size()];
            for (int i = 0; i < vibrateArray.size(); i++) {
                vibrate[i] = vibrateArray.get(i);
            }
            nt.vibrate = vibrate;
        } else {
            nt.defaults |= Notification.DEFAULT_VIBRATE;
            nt.flags |= Notification.FLAG_INSISTENT;
        }
        int soundId = new Random(System.currentTimeMillis())
                .nextInt(Integer.MAX_VALUE);
        mgr.notify(soundId, nt);
        return soundId;
    }

    public static PendingIntent getDefalutIntent(final Context context, int flags){
        PendingIntent pendingIntent = PendingIntent.getActivity(context, 1, new Intent(), flags);
        return pendingIntent;
    }

    private void playAlarmRing(final Context context) {
        Uri uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM);
        try {
            mMediaPlayer = new MediaPlayer();
            mMediaPlayer.setDataSource(context, uri);
            final AudioManager audioManager = (AudioManager) context
                    .getSystemService(Context.AUDIO_SERVICE);
            if (audioManager.getStreamVolume(AudioManager.STREAM_ALARM) != 0) {
                mMediaPlayer.setAudioStreamType(AudioManager.STREAM_ALARM);
                mMediaPlayer.setLooping(true);
                mMediaPlayer.prepare();
            }
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        mMediaPlayer.start();
    }

    private void StopAlarmRing() {
        mMediaPlayer.stop();
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        int pos = SharedPreferencesUtil.getInt(context, Config.VIBRATE_DURATION, 0);
        int vibrateDuration = 1;
        String[] durations = context.getResources().getStringArray(R.array.vibrate_duration);
        if (durations[pos].equals("10s")) {
            vibrateDuration = 5;
        } else if (durations[pos].equals("30s")) {
            vibrateDuration = 15;
        }
        PlaySound(context, vibrateDuration);
    }

}