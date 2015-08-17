package cn.edu.tsinghua.thss.popcorn.ui;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.media.Image;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.ViewInject;
import com.lidroid.xutils.view.annotation.event.OnClick;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;

import cn.edu.tsinghua.thss.popcorn.AboutInfoActivity;
import cn.edu.tsinghua.thss.popcorn.ChangePasswordActivity;
import cn.edu.tsinghua.thss.popcorn.FeedBackActivity;
import cn.edu.tsinghua.thss.popcorn.R;
import cn.edu.tsinghua.thss.popcorn.UserInfoActivity;
import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.update.UpdateInfoParser;


/**
 * @author wenqingfu
 * @email thssvince@163.com
 */

public class MineFragment extends Fragment {

    private static int UPDATE_VERSION = 2;
    private View mineView;
    private String localVersion = "", remoteVersion = "";

    @ViewInject(R.id.id_tab_mine_avatar)
    private ImageView mineAvatar;

    @ViewInject(R.id.mine_name)
    private TextView myName;

    @ViewInject(R.id.mine_username)
    private TextView myUserName;

    @ViewInject(R.id.tab_mine_about_hint)
    private TextView aboutHint;

    @OnClick(R.id.mine_user_info)
    private void onShowUserInfo(View v){
        Intent intent = new Intent(getActivity(), UserInfoActivity.class);
        Bundle bundle = new Bundle();
        intent.putExtras(bundle);
        startActivity(intent);
    }

    @OnClick(R.id.change_password)
    private void onChangePsdClick(View v) {
        Intent intent = new Intent(getActivity(), ChangePasswordActivity.class);
        Bundle bundle = new Bundle();
        intent.putExtras(bundle);
        startActivity(intent);
    }

    @OnClick(R.id.feed_back)
    private void onFeedBackClick(View v) {
        Intent intent = new Intent(getActivity(), FeedBackActivity.class);
        Bundle bundle = new Bundle();
        intent.putExtras(bundle);
        startActivity(intent);
    }

    @OnClick(R.id.about_info)
    private void onAboutInfoClick(View v) {
        Intent intent = new Intent(getActivity(), AboutInfoActivity.class);
        Bundle bundle = new Bundle();
        intent.putExtras(bundle);
        startActivity(intent);
    }

    @OnClick(R.id.log_out)
    private void onLogOutClick(View v){
        SharedPreferences sp = getActivity().getApplicationContext().getSharedPreferences("userInfo", Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = sp.edit();
        editor.putString("USERNAME", "");
        editor.putString("PASSWORD", "");
        editor.putString("ACCESS_TOKEN", "");
        editor.apply();
        getActivity().finish();
    }

    @Override
    public View onCreateView(LayoutInflater inflater,ViewGroup container,Bundle savedInstanceState){
        super.onCreateView(inflater, container, savedInstanceState);

        if(mineView==null){
            mineView=inflater.inflate(R.layout.activity_tab_mine, null);
        }

        ViewGroup parent = (ViewGroup) mineView.getParent();
        if (parent != null) {
            parent.removeView(mineView);
        }
        ViewUtils.inject(this, mineView);

        return mineView;
    }

    @Override
    public void onStart(){
        super.onStart();
        checkVersionUpdate();
        getUserInfo();
    }


    public String getVersionName() throws Exception {
        PackageManager packageManager = getActivity().getPackageManager();
        PackageInfo packInfo = packageManager.getPackageInfo(getActivity().getPackageName(),
                0);
        return packInfo.versionName;
    }


    private void checkVersionUpdate(){
        try {
            localVersion = getVersionName();
        }catch (Exception e) {
            e.printStackTrace();
        }

        new Thread(){
            @Override
            public void run() {
                // TODO Auto-generated method stub
                super.run();
                remoteVersion = UpdateInfoParser.getRemoteVersion();
                Message message = new Message();
                message.what = UPDATE_VERSION;
                handler.sendMessage(message);
            }
        }.start();
    }

    Handler handler = new Handler() {
        public void handleMessage(Message msg) {
            if (msg.what == UPDATE_VERSION){
                if(remoteVersion.equals("") || remoteVersion.equals(localVersion)){
                    aboutHint.setVisibility(View.GONE);
                }else{
                    aboutHint.setVisibility(View.VISIBLE);
                }
            }
            super.handleMessage(msg);
        };
    };
    private void getUserInfo(){
        Bitmap photo = getDiskBitmap(Config.AVATAR_FILE_DIR +Config.DEBUG_USERNAME+".jpg");
        if(photo!=null){
            //Drawable drawable = new BitmapDrawable(this.getResources(),photo);
            mineAvatar.setImageBitmap(photo);
        }

        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.GET_USER_INFO_URL,
                params,
                new RequestCallBack<String>() {

                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try {
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");


                            if (status.equals("ok")) {
                                JSONObject userInfo = jsonObject.getJSONObject("data");
                                String name = userInfo.getString("name");
                                myName.setText(name);
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                        myUserName.setText(Config.DEBUG_USERNAME);
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getActivity().getApplicationContext(), "网络故障", Toast.LENGTH_SHORT).show();
                    }
                });
    }

    @Override
    public void onActivityCreated(Bundle savedInstanceState){
        super.onActivityCreated(savedInstanceState);
    }

    private Bitmap getDiskBitmap(String pathString)
    {
        Bitmap bitmap = null;
        try
        {
            File file = new File(pathString);
            if(file.exists())
            {
                bitmap = BitmapFactory.decodeFile(pathString);
            }
        } catch (Exception e)
        {
            // TODO: handle exception
        }
        return bitmap;
    }
}
