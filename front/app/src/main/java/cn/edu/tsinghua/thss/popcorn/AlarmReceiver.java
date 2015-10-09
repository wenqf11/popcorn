package cn.edu.tsinghua.thss.popcorn;

import android.app.Notification;
import android.app.NotificationManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.media.RingtoneManager;
import android.net.Uri;
import android.widget.Toast;

import java.io.IOException;
import java.util.Random;

/**
 * Created by vince on 2015/8/18.
 */
public class AlarmReceiver extends BroadcastReceiver {
    private MediaPlayer mMediaPlayer;

    public static int PlaySound(final Context context) {
        NotificationManager mgr = (NotificationManager) context
                .getSystemService(Context.NOTIFICATION_SERVICE);
        Notification nt = new Notification();
        nt.defaults = Notification.DEFAULT_SOUND;
        int soundId = new Random(System.currentTimeMillis())
                .nextInt(Integer.MAX_VALUE);
        mgr.notify(soundId, nt);
        return soundId;
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
        PlaySound(context);
        //playAlarmRing(context);
        Toast.makeText(context, "您有新的任务，请尽快完成~~", Toast.LENGTH_LONG).show();
    }

}